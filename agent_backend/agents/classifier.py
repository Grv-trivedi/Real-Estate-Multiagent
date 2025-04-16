from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def classify_text_message(user_msg: str, history: list) -> str:
    messages = [
        SystemMessage(
            content="You are a message classifier. Your goal is to only Classify the user's message into one of these categories:\n1: Property Issue (visible problems, maintenance, images)\n2: Tenancy FAQ (rent, landlord rights, contracts)\n3: Unclear (needs clarification).Return ONLY the number."
        )
    ]

    for h in history:
        messages.append(
            HumanMessage(content=h["content"])
            if h["role"] == "user"
            else AIMessage(content=h["content"])
        )

    messages.append(HumanMessage(content=user_msg))

    result = await llm.ainvoke(messages)
    return result.content.strip()


async def get_clarifying_question(user_msg: str, history: list) -> str:
    messages = [
        SystemMessage(
            content="You're a helpful assistant that helps users clarify their request."
        )
    ]

    for h in history:
        messages.append(
            HumanMessage(content=h["content"])
            if h["role"] == "user"
            else AIMessage(content=h["content"])
        )

    messages.append(
        HumanMessage(
            content=f"""
    A user said: \"{user_msg}\"
    It's unclear if they are asking about a property issue (like mold, water damage, etc.)
    or a rental/legal FAQ (like rent, landlord rights, etc.)
    Ask a short, polite, follow-up question to clarify.
    """
        )
    )

    result = await llm.ainvoke(messages)
    return result.content.strip()
