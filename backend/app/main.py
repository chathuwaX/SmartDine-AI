from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import traceback
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from .database.database import engine, Base, get_db
from .database.seed import seed_database
from .database import models
from .agent.agent import create_chat_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup tasks."""
    db = next(get_db())
    seed_database(db)
    print("Database seeded successfully.")
    yield


app = FastAPI(title="SmartDine AI Backend", lifespan=lifespan)

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str


class ClearChat(BaseModel):
    pass


# In-memory store for chat sessions (simple demo approach)
chat_sessions = {}


@app.post("/chat")
def chat_with_agent(req: ChatMessage):
    session_id = "default"
    if session_id not in chat_sessions:
        chat_sessions[session_id] = create_chat_session()

    chat = chat_sessions[session_id]

    try:
        response = chat.send_message(req.message)
        return {"response": response.text, "status": "success"}
    except Exception as e:
        error_msg = str(e)
        print(f"Error in chat: {error_msg}")
        traceback.print_exc()
        # Reset the session so the next message starts fresh
        chat_sessions.pop(session_id, None)
        return {"response": f"Sorry, something went wrong: {error_msg}", "status": "error"}


@app.post("/chat/clear")
def clear_chat():
    """Clear the chat session to start a new conversation."""
    chat_sessions.pop("default", None)
    return {"status": "cleared"}


@app.get("/menu")
def get_menu(db: Session = Depends(get_db)):
    items = db.query(models.MenuItem).all()
    return items


@app.get("/restaurant")
def get_restaurant_info():
    return {
        "name": "SmartDine Restaurant",
        "description": "Good Food. Smart Assistance."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
