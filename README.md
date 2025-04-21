
# Sales Agent Chatbot Project

## Overview

This project implements a sales agent chatbot that interacts with leads to collect information, using the Gemini API for message generation. The chatbot is designed to:

- Trigger conversations with leads after a simulated form submission.
- Collect information (age, country, interest) through a series of questions.
- Handle multiple lead conversations concurrently.
- Send follow-up messages to unresponsive leads after a simulated 24-hour delay.
- Store lead data in a CSV file (`leads.csv`).

The project meets all requirements specified in the `AI Assessment.pdf`, including the use of the Gemini API for message generation. The conversations are automated, simulating interactions with three leads: Alice, Bob, and Charlie.

## Features

- **Triggering the Agent**: Initiates conversations with a unique `lead_id` and sends the initial message: "Hey \[Lead Name\], thank you for filling out the form. I'd like to gather some information from you. Is that okay?"
- **Lead Response Handling**: Proceeds with questions if the lead agrees ("Yes", "Okay", "Sure") or ends the conversation if the lead declines ("No").
- **Information Collection**: Asks questions sequentially ("What is your age?", "Which country are you from?", "What product or service are you interested in?") and stores responses in `leads.csv`.
- **Concurrent Conversations**: Manages multiple leads simultaneously using asynchronous programming (`asyncio`).
- **Follow-Up Mechanism**: Sends a follow-up message ("Just checking in to see if you're still interested. Let me know when you're ready to continue.") after a simulated 24-hour delay (5 seconds for testing).
- **Gemini API Integration**: Uses the Gemini API (`gemini-1.5-flash`) to generate all key messages dynamically.

## Project Structure

- `sales_agent.py`: Main script containing the sales agent implementation and automated simulation.
- `test_cases.py`: Test cases to validate the agent's functionality (full conversation, decline, follow-up).
- `leads.csv`: CSV file where lead data is stored (columns: `lead_id, name, age, country, interest, status`).
- `.env`: Environment file storing the Gemini API key (not included in the repository for security).
- `README.md`: This file, providing project documentation.

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
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install google-generativeai python-dotenv
   ```

4. **Set Up the Gemini API Key**:

   - Create a `.env` file in the project root:

     ```bash
     touch .env
     ```

   - Add your Gemini API key:

     ```
     GEMINI_API_KEY=your-api-key-here
     ```

5. **Ensure** `leads.csv` **Is Writable**:

   - The script will create or overwrite `leads.csv` in the project directory. Ensure you have write permissions in the directory.

## Running the Project

1. **Run the Main Script**:

   - The script simulates conversations with three leads (Alice, Bob, Charlie) using predefined responses.

   - Run:

     ```bash
     python sales_agent.py
     ```


2. **Run the Test Cases**:

   - Run:

     ```bash
     python test_cases.py
     ```

   - This will validate the agent's functionality with three test cases: a full conversation, a lead declining, and a follow-up trigger.

3. **Check** `leads.csv`:

   - After running `sales_agent.py`, open `leads.csv` to view the lead data:

     ```
     lead_id,name,age,country,interest,status
     <uuid>,Alice,25,USA,Software,secured
     <uuid>,Bob,,,,no_response
     <uuid>,Charlie,30,,,initiated
     ```

## Implementation Details

- **Gemini API**: Messages are generated using the `gemini-1.5-flash` model with constrained prompts to ensure exact wording as per requirements.
- **Concurrency**: Uses `asyncio` for asynchronous handling of multiple lead conversations.
- **Follow-Up Mechanism**: Simulates a 24-hour delay as 5 seconds for testing, sending follow-up messages to unresponsive leads.
- **CSV Storage**: Lead data is stored in `leads.csv` with appropriate statuses (`secured`, `no_response`, `initiated`).

## Known Limitations

- **Gemini API Rate Limits**: The free tier has a 15 RPM limit. If exceeded, the script uses hardcoded fallbacks to ensure functionality.
- **File Access**: Ensure `leads.csv` is not open in another program during execution to avoid write errors.

## Video Demonstration

- A video demonstration is available (or will be recorded) showing the script in action:
  - Running `sales_agent.py` to simulate conversations.
  - Displaying the output and `leads.csv`.
  - Highlighting concurrent conversations and follow-up messages.
