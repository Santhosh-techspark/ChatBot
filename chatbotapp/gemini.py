import os
from groq import Groq

MODEL_NAME = "openai/gpt-oss-120b"

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment")
        _client = Groq(api_key=api_key)
    return _client


def get_ai_reply(message, history_text="", document_text=""):
    client = get_client()  # ✅ ALWAYS get a valid client

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
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.4,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()
