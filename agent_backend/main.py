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
        parsed_history = json.loads(history)
        # ROUTING STEP 1: If image is uploaded, go to Agent 1
        if image:
            image_bytes = await image.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            response = await get_issue_detection_response(message, image_b64, parsed_history)
            return {"response": response}

        # ROUTING STEP 2: Classify the message with conversation context
        classification = await classify_text_message(message, parsed_history)

        print(f"Classification: {classification}")
        if classification == "1":
            response = await get_issue_detection_response(message, image_b64=None, history=parsed_history)
        elif classification == "2":
            response = await get_tenancy_faq_response(message, parsed_history)
        else:
            response = await get_clarifying_question(message, parsed_history)
        return {"response": response}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
