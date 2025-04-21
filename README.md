# Sales Agent Chatbot Project

## Overview
This project implements a sales agent chatbot that interacts with leads to collect information, using the Gemini API for message generation. The chatbot is designed to:
- Trigger conversations with leads after a simulated form submission.
- Collect information (age, country, interest) through a series of questions.
- Handle multiple lead conversations concurrently.
- Send follow-up messages to unresponsive leads after a simulated 24-hour delay.
- Store lead data in a CSV file (`leads.csv`).

The project meets all requirements specified in the `AI Assessment.pdf`, including the use of the Gemini API for message generation.

## Features
- **Triggering the Agent**: Initiates conversations with a unique `lead_id` and sends the initial message: "Hey [Lead Name], thank you for filling out the form. I'd like to gather some information from you. Is that okay?"
- **Lead Response Handling**: Proceeds with questions if the lead agrees ("Yes", "Okay", "Sure") or ends the conversation if the lead declines ("No").
- **Information Collection**: Asks questions sequentially ("What is your age?", "Which country are you from?", "What product or service are you interested in?") and stores responses in `leads.csv`.
- **Concurrent Conversations**: Manages multiple leads simultaneously using asynchronous programming (`asyncio`).
- **Follow-Up Mechanism**: Sends a follow-up message ("Just checking in to see if you're still interested. Let me know when you're ready to continue.") after a simulated 24-hour delay (5 seconds for testing).
- **Gemini API Integration**: Uses the Gemini API (`gemini-1.5-flash`) to generate all key messages dynamically.

## Project Structure
- **`sales_agent.py`**: Main script containing the sales agent implementation and automated simulation.
- **`test_cases.py`**: Test cases to validate the agent's functionality (full conversation, decline, follow-up).
- **`leads.csv`**: CSV file where lead data is stored (columns: `lead_id, name, age, country, interest, status`).
- **`.env`**: Environment file storing the Gemini API key (not included in the repository for security).
- **`README.md`**: This file, providing project documentation.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed.
- **Virtual Environment**: Recommended for dependency management.
- **Dependencies**:
  - `google-generativeai`: For Gemini API integration.
  - `python-dotenv`: For loading environment variables.
- **Gemini API Key**: Obtain an API key from Google and store it in a `.env` file.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd sales-agent-project
Set Up a Virtual Environment:
bash

Copy
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install Dependencies:
bash

Copy
pip install google-generativeai python-dotenv
Set Up the Gemini API Key:
Create a .env file in the project root:
bash

Copy
touch .env
Add your Gemini API key:
text

Copy
GEMINI_API_KEY=your-api-key-here
Ensure leads.csv Is Writable:
The script will create or overwrite leads.csv in the project directory. Ensure you have write permissions in the directory.
Running the Project
Run the Main Script:
The script simulates conversations with three leads (Alice, Bob, Charlie) using predefined responses.
Run:
bash

Copy
python sales_agent.py
Expected Output:
text

Copy
INFO:__main__:Cleared leads.csv for new run
Agent response to Alice: Hey Alice, thank you for filling out the form. I'd like to gather some information from you. Is that okay?
Lead Alice input: Yes
Agent response to Alice: What is your age?
Lead Alice input: 25
Agent response to Alice: Which country are you from?
Lead Alice input: USA
Agent response to Alice: What product or service are you interested in?
Lead Alice input: Software
Agent response to Bob: Hey Bob, thank you for filling out the form. I'd like to gather some information from you. Is that okay?
Lead Bob input: No
Agent response to Charlie: Hey Charlie, thank you for filling out the form. I'd like to gather some information from you. Is that okay?
Lead Charlie input: Yes
Agent response to Charlie: What is your age?
Lead Charlie input: 30
Agent response to Charlie: Which country are you from?
Agent response to Bob: Alright, no problem. Have a great day!
INFO:__main__:Wrote to leads.csv: {'lead_id': '...', 'name': 'Bob', ...}
Agent response to Alice: Thank you for providing the information!
INFO:__main__:Wrote to leads.csv: {'lead_id': '...', 'name': 'Alice', ...}
INFO:__main__:Sending follow-up to lead ...
INFO:__main__:Wrote to leads.csv: {'lead_id': '...', 'name': 'Charlie', ...}
Follow-up: ...: Just checking in to see if you're still interested. Let me know when you're ready to continue.
Run the Test Cases:
Run:
bash

Copy
python test_cases.py
This will validate the agent's functionality with three test cases: a full conversation, a lead declining, and a follow-up trigger.
Check leads.csv:
After running sales_agent.py, open leads.csv to view the lead data:
text

Copy
lead_id,name,age,country,interest,status
<uuid>,Alice,25,USA,Software,secured
<uuid>,Bob,,,,no_response
<uuid>,Charlie,30,,,initiated
Implementation Details
Gemini API: Messages are generated using the gemini-1.5-flash model with constrained prompts to ensure exact wording as per requirements.
Concurrency: Uses asyncio for asynchronous handling of multiple lead conversations.
Follow-Up Mechanism: Simulates a 24-hour delay as 5 seconds for testing, sending follow-up messages to unresponsive leads.
CSV Storage: Lead data is stored in leads.csv with appropriate statuses (secured, no_response, initiated).
Known Limitations
Gemini API Rate Limits: The free tier has a 15 RPM limit. If exceeded, the script uses hardcoded fallbacks to ensure functionality.
File Access: Ensure leads.csv is not open in another program during execution to avoid write errors.
Video Demonstration
A video demonstration is available (or will be recorded) showing the script in action:
Running sales_agent.py to simulate conversations.
Displaying the output and leads.csv.
Highlighting concurrent conversations and follow-up messages.
