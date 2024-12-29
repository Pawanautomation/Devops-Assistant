from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="DevOps Teaching Assistant")

# Initialize Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)

class Question(BaseModel):
    text: str
    topic: Optional[str] = None
    difficulty: Optional[str] = None

@app.post("/ask")
async def ask_question(question: Question):
    try:
        # Store question in Supabase
        result = supabase.table("questions").insert({
            "text": question.text,
            "topic": question.topic,
            "difficulty": question.difficulty
        }).execute()

        # TODO: Add LLaMA integration here
        # For now, return a mock response
        return {
            "status": "success",
            "question_id": result.data[0]["id"],
            "message": "Question received and stored successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}