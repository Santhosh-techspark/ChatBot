import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
client = None

def get_client():
    global client
    if client is None:
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found. Please set it in your environment variables.")
        client = Groq(api_key=api_key)
    return client

MODEL_NAME = "openai/gpt-oss-120b"


def get_ai_reply(message, history_text="", document_text=""):
    # ✅ Always include chat history
    if document_text.strip():
        prompt = f"""
You are a helpful AI assistant.

DOCUMENT CONTENT:
{document_text}

CHAT HISTORY:
{history_text}

User question:
{message}

Rules:
- Answer using document if relevant
- Otherwise use chat history
- Be concise and clear
"""
    else:
        prompt = f"""
You are a helpful AI assistant.

CHAT HISTORY:
{history_text}

User question:
{message}

Rules:
- Use chat history to answer
- If user already stated a fact, remember it
- Answer naturally
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()
