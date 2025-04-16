from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import base64
import json
import os
from dotenv import load_dotenv

from agents.issue_detector import get_issue_detection_response
from agents.faq_agent import get_tenancy_faq_response
from agents.classifier import classify_text_message, get_clarifying_question


# Load environment variables
load_dotenv()

# FastAPI app initialization
app = FastAPI()

# Get the OpenAI API Key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# openai.api_key = openai_api_key


app = FastAPI()

# Enable CORS for all origins (adjust for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(
    message: str = Form(...),
    image: UploadFile = File(default=None),
    history: str = Form(default="[]"),  # JSON stringified array of { role, content }
):
    try:
        return {"response": "This is a test response from gaurav."}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
