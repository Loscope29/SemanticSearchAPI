import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Tu es un assistant pédagogique.
Tu dois répondre uniquement à partir du CONTEXTE fourni.
Si l'information n'est pas dans le contexte, dis clairement que tu ne sais pas.
"""

def generate_rag_answer(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)

    prompt = f"""
CONTEXTE :
{context}

QUESTION :
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
