import os

from google import genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key='GEMINI_API_KEY')

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

    response =  client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        config={
            'temperature': 0,
            'top_p': 0.95,
            'top_k': 20,
            'max_token' : 2000,
        }
    )

    return response.choices[0].message.content
