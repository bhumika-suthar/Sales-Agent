import asyncio
import csv
import os
from datetime import datetime
from typing import Dict
import uuid
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Configuration
LEADS_CSV = "leads.csv"
FOLLOW_UP_INTERVAL = 5.0  # Simulated 24 hours as 5 seconds for testing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadState:
    def __init__(self, lead_id: str, name: str):
        self.lead_id = lead_id
        self.name = name
        self.status = "initiated"
        self.current_question = 0
        self.responses = {}
        self.last_interaction = datetime.now()
        self.consent = False

class SalesAgent:
    def __init__(self):
        self.lead_states: Dict[str, LeadState] = {}
        self.questions = [
            "What is your age?",
            "Which country are you from?",
            "What product or service are you interested in?"
        ]
        self.fieldnames = ['lead_id', 'name', 'age', 'country', 'interest', 'status']
        
        # Overwrite CSV to start fresh
        try:
            with open(LEADS_CSV, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
            logger.info(f"Cleared {LEADS_CSV} for new run")
        except Exception as e:
            logger.error(f"Error clearing {LEADS_CSV}: {e}")
            raise

    async def generate_message(self, message_type: str, name: str = None) -> str:
        try:
            if message_type == "initial":
                prompt = f"Generate the exact message: 'Hey {name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?' Do not modify the wording."
                response = await asyncio.to_thread(model.generate_content, prompt)
                return response.text.strip()
            elif message_type == "decline":
                prompt = "Generate the exact message: 'Alright, no problem. Have a great day!' Do not modify the wording."
                response = await asyncio.to_thread(model.generate_content, prompt)
                return response.text.strip()
            elif message_type == "thank_you":
                prompt = "Generate the exact message: 'Thank you for providing the information!' Do not modify the wording."
                response = await asyncio.to_thread(model.generate_content, prompt)
                return response.text.strip()
            elif message_type == "follow_up":
                prompt = "Generate the exact message: 'Just checking in to see if you're still interested. Let me know when you're ready to continue.' Do not modify the wording."
                response = await asyncio.to_thread(model.generate_content, prompt)
                return response.text.strip()
            else:
                return "Unknown message type."
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            # Fallbacks to ensure functionality
            if message_type == "initial":
                return f"Hey {name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?"
            elif message_type == "decline":
                return "Alright, no problem. Have a great day!"
            elif message_type == "thank_you":
                return "Thank you for providing the information!"
            elif message_type == "follow_up":
                return "Just checking in to see if you're still interested. Let me know when you're ready to continue."
            return "Error generating message."

    async def handle_lead(self, lead_id: str, user_input: str, name: str) -> str:
        # Initialize new lead
        if lead_id not in self.lead_states:
            self.lead_states[lead_id] = LeadState(lead_id, name)
            return await self.generate_message("initial", name)

        lead_state = self.lead_states[lead_id]
        lead_state.last_interaction = datetime.now()

        # Handle consent response
        if not lead_state.consent:
            if user_input.lower() in ['yes', 'okay', 'sure']:
                lead_state.consent = True
                return self.questions[0]  # Start with first question
            else:
                lead_state.status = "no_response"
                self._write_to_csv(lead_state)
                return await self.generate_message("decline")

        # Handle question responses
        if lead_state.current_question < len(self.questions):
            response_key = self.fieldnames[lead_state.current_question + 2]  # Map to age, country, interest
            lead_state.responses[response_key] = user_input
            lead_state.current_question += 1

            if lead_state.current_question < len(self.questions):
                return self.questions[lead_state.current_question]
            else:
                lead_state.status = "secured"
                self._write_to_csv(lead_state)
                return await self.generate_message("thank_you")

        return "Conversation completed."

    def _write_to_csv(self, lead_state: LeadState):
        row = {
            'lead_id': lead_state.lead_id,
            'name': lead_state.name,
            'age': lead_state.responses.get('age', ''),
            'country': lead_state.responses.get('country', ''),
            'interest': lead_state.responses.get('interest', ''),
            'status': lead_state.status
        }
        try:
            with open(LEADS_CSV, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(row)
                f.flush()  # Force flush to ensure data is written
            logger.info(f"Wrote to {LEADS_CSV}: {row}")
        except Exception as e:
            logger.error(f"Error writing to {LEADS_CSV}: {e}")
            raise

    async def check_follow_ups(self, simulated_delay: float = FOLLOW_UP_INTERVAL):
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < simulated_delay + 2:  # Run for delay + buffer
            current_time = datetime.now()
            for lead_id, lead_state in self.lead_states.items():
                if lead_state.status not in ["secured", "no_response"] and lead_state.consent:
                    time_diff = (current_time - lead_state.last_interaction).total_seconds()
                    if time_diff >= simulated_delay:
                        logger.info(f"Sending follow-up to lead {lead_id}")
                        # Write partial data to CSV with status 'initiated'
                        if lead_state.current_question > 0:
                            lead_state.status = "initiated"
                            self._write_to_csv(lead_state)
                        follow_up_message = await self.generate_message("follow_up")
                        yield f"{lead_id}: {follow_up_message}"
                        lead_state.last_interaction = current_time
            await asyncio.sleep(1.0)

# Simulation script
async def simulate_lead_interactions():
    agent = SalesAgent()
    
    # Simulate multiple leads
    leads = [
        {"lead_id": str(uuid.uuid4()), "name": "Alice", "responses": ["Yes", "25", "USA", "Software"]},
        {"lead_id": str(uuid.uuid4()), "name": "Bob", "responses": ["No"]},
        {"lead_id": str(uuid.uuid4()), "name": "Charlie", "responses": ["Yes", "30"]}  # Will trigger follow-up
    ]

    # Handle concurrent conversations
    async def process_lead(lead):
        lead_id = lead["lead_id"]
        name = lead["name"]
        # Send initial message
        response_text = await agent.handle_lead(lead_id, "", name)  # Empty input to trigger initial message
        print(f"Agent response to {name}: {response_text}")
        for response in lead["responses"]:
            print(f"Lead {name} input: {response}")
            response_text = await agent.handle_lead(lead_id, response, name)
            print(f"Agent response to {name}: {response_text}")

    # Run conversations concurrently
    tasks = [process_lead(lead) for lead in leads]
    await asyncio.gather(*tasks)

    # Simulate follow-up check with enough time
    async for follow_up in agent.check_follow_ups():
        print(f"Follow-up: {follow_up}")

if __name__ == "__main__":
    asyncio.run(simulate_lead_interactions())