import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from dotenv import load_dotenv

# Get the OpenAI API Key from environment variables
# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm2 = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def get_issue_detection_response(
    message: str, image_b64: str = None, history: list = []
) -> str:
    messages = [
        SystemMessage(
            content="You are a property Issue Detection and Troubleshooting assistant. Detect visible issues from user-uploaded property images and text, and suggest fixes. Ask clarifying follow-up questions to diagnose better"
        )
    ]

    for h in history:
        messages.append(
            HumanMessage(content=h["content"])
            if h["role"] == "user"
            else AIMessage(content=h["content"])
        )

    if image_b64:
        messages.append(
            HumanMessage(
                content=[
                    {"type": "text", "text": message},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                ]
            )
        )
    else:
        messages.append(HumanMessage(content=message))

    result = await llm.ainvoke(messages) if image_b64 else await llm2.ainvoke(messages)
    return result.content.strip()
