# SmartDine AI - Restaurant Chatbot and Agent

SmartDine AI is a modern restaurant web application that demonstrates the capabilities of an AI Agent. Unlike a simple chatbot, the SmartDine AI agent can understand user intents and intelligently decide when to use specific backend tools to interact with the restaurant's menu and reservation systems.

## Features

- **Menu Browsing:** Explore the restaurant's menu with prices and vegetarian options.
- **AI Agent Chatbot:** A natural conversational interface.
- **Tool Selection & Execution:** The AI automatically selects and runs tools for:
  - Menu searching
  - Food recommendations based on preferences/budget
  - Calculating exact order costs based on real menu prices
  - Checking table availability
  - Making reservations
  - Providing static restaurant information

## Architecture

This project follows a decoupled client-server architecture:

```
User -> React Chat UI -> FastAPI Backend -> Google ADK Agent (Gemini API) -> Tools (SQLite)
```

## Chatbot vs AI Agent

### Chatbot
A normal chatbot uses a Large Language Model (LLM) to generate text based solely on the patterns it learned during training. It might hallucinate prices or invent menu items because it lacks real-world connectivity.

### AI Agent
An AI Agent acts autonomously by interacting with its environment. When a user asks for a price calculation, the SmartDine Agent doesn't try to guess the answer. Instead, it:
1. **Understands the intent** (calculating an order).
2. **Decides** to use the `calculate_order` tool.
3. **Executes** the tool by querying the SQLite database.
4. **Receives** the exact total cost.
5. **Generates** a natural language response using the precise data retrieved.

## Technologies

- **Frontend:** React, Vite, Tailwind CSS, Lucide React
- **Backend:** FastAPI, Uvicorn, SQLAlchemy, SQLite
- **AI Integration:** Google Agent Development Kit (google-genai) using Gemini 2.5 Flash

## Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js (for frontend)
- A Google Gemini API Key from Google AI Studio (Free Tier)

### 1. Clone & Configure the Project
Navigate to the root directory `SmartDine-AI`.

Create a `.env` file in the `backend` folder and add your API key:
```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### 2. Backend Setup
Open a terminal (e.g., PowerShell) and navigate to the backend directory:
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Frontend Setup
Open a new terminal and navigate to the frontend directory:
```powershell
cd frontend
npm install
npm run dev
```

## Example Prompts for Testing
Try asking the AI Assistant these questions to see tool usage in action:
1. "Hello" (General chat)
2. "What vegetarian food do you have?" (Triggers menu search)
3. "Recommend something under Rs. 1500." (Triggers recommendation tool)
4. "How much are two chicken burgers and two Cokes?" (Triggers calculation tool)
5. "Can I book a table for 4 people tomorrow at 7 PM?" (Triggers table availability tool)
6. "Book it under the name John." (Triggers reservation tool)
7. "What are your opening hours?" (Triggers restaurant info tool)

## Security Considerations
- The `.env` file containing the API key is excluded via `.gitignore`.
- API keys are never exposed in the frontend codebase.
- User input is parameterized via SQLite and SQLAlchemy to prevent SQL injection.
- The AI is instructed not to invent data, ensuring reliability.

## Future Improvements
- **LangGraph/CrewAI Integration:** For complex multi-agent workflows.
- **PostgreSQL:** For robust concurrent database operations.
- **Authentication:** For user accounts and order history.
