from sentence_transformers import SentenceTransformer
import numpy as np

from pypdf import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text



model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    emb = model.encode(text)
    emb = emb / np.linalg.norm(emb)
    return emb.tolist()
