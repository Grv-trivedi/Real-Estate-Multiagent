from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def get_tenancy_faq_response(message: str, history: list) -> str:
    messages = [
        SystemMessage(
            content="You are a real estate legal assistant that answers tenancy and rental-related questions.You are Capable of giving location-specific guidance if the user's city or country is provided."
        )
    ]

    for h in history:
        messages.append(
            HumanMessage(content=h["content"])
            if h["role"] == "user"
            else AIMessage(content=h["content"])
        )

    messages.append(HumanMessage(content=message))

    result = await llm.ainvoke(messages)
    return result.content.strip()
