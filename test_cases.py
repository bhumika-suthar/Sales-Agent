import asyncio
import uuid
import csv
import os
from sales_agent import SalesAgent

async def run_test_cases():
    # Test Case 1: Full conversation with consent
    agent = SalesAgent()
    lead_id1 = str(uuid.uuid4())
    responses1 = ["Yes", "28", "Canada", "Cloud Services"]
    print("Test Case 1: Full conversation")
    # Initial message with Gemini-generated greeting
    initial_message = await agent.handle_lead(lead_id1, "", "David")
    print(f"Agent: {initial_message}")
    # Verify the required initial message is present (ignore greeting)
    assert "Hey David, thank you for filling out the form. I'd like to gather some information from you. Is that okay?" in initial_message
    
    for response in responses1:
        print(f"Lead David input: {response}")
        result = await agent.handle_lead(lead_id1, response, "David")
        print(f"Agent: {result}")
        if response == "Yes":
            assert result == "What is your age?"
        elif response == "28":
            assert result == "Which country are you from?"
        elif response == "Canada":
            assert result == "What product or service are you interested in?"
        elif response == "Cloud Services":
            assert result == "Thank you for providing the information!"

    # Verify CSV for Test Case 1
    with open("leads.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['lead_id'] == lead_id1:
                assert row['name'] == "David"
                assert row['age'] == "28"
                assert row['country'] == "Canada"
                assert row['interest'] == "Cloud Services"
                assert row['status'] == "secured"
                break

    # Test Case 2: Lead declines
    agent = SalesAgent()  # Reset agent to clear CSV
    lead_id2 = str(uuid.uuid4())
    print("\nTest Case 2: Lead declines")
    # Initial message
    initial_message = await agent.handle_lead(lead_id2, "", "Eve")
    print(f"Agent: {initial_message}")
    assert "Hey Eve, thank you for filling out the form. I'd like to gather some information from you. Is that okay?" in initial_message
    
    decline_response = await agent.handle_lead(lead_id2, "No", "Eve")
    print(f"Lead Eve input: No")
    print(f"Agent: {decline_response}")
    assert decline_response == "Alright, no problem. Have a great day!"

    # Verify CSV for Test Case 2
    with open("leads.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['lead_id'] == lead_id2:
                assert row['name'] == "Eve"
                assert row['age'] == ""
                assert row['country'] == ""
                assert row['interest'] == ""
                assert row['status'] == "no_response"
                break

    # Test Case 3: Follow-up trigger with partial data
    agent = SalesAgent()  # Reset agent to clear CSV
    lead_id3 = str(uuid.uuid4())
    print("\nTest Case 3: Follow-up trigger")
    # Initial message
    initial_message = await agent.handle_lead(lead_id3, "", "Frank")
    print(f"Agent: {initial_message}")
    assert "Hey Frank, thank you for filling out the form. I'd like to gather some information from you. Is that okay?" in initial_message
    
    consent_response = await agent.handle_lead(lead_id3, "Yes", "Frank")
    print(f"Lead Frank input: Yes")
    print(f"Agent: {consent_response}")
    assert consent_response == "What is your age?"
    
    age_response = await agent.handle_lead(lead_id3, "30", "Frank")
    print(f"Lead Frank input: 30")
    print(f"Agent: {age_response}")
    assert age_response == "Which country are you from?"
    
    # Simulate follow-up after delay
    async for follow_up in agent.check_follow_ups(simulated_delay=0.1):
        print(f"Follow-up: {follow_up}")
        assert "Just checking in to see if you're still interested. Let me know when you're ready to continue." in follow_up
        break

    # Verify CSV for Test Case 3
    with open("leads.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['lead_id'] == lead_id3:
                assert row['name'] == "Frank"
                assert row['age'] == "30"
                assert row['country'] == ""
                assert row['interest'] == ""
                assert row['status'] == "initiated"
                break

if __name__ == "__main__":
    asyncio.run(run_test_cases())