import pdfplumber
import re
import docx

def extract_pdf(pdf_file):
    """Extrait le texte d'un fichier PDF"""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction du texte: {str(e)}")
    return text

def extract_txt(file):
    """Extrait le texte d'un fichier txt"""
    return file.read().decode("utf-8")

def extract_docx(file):
    doc = docx.Document(file)
    return " ".join([p.text for p in doc.paragraphs])

def extract_text(file):
    name = file.name.lower()
    if name.endswith(".pdf"):
        return extract_text(file)
    if name.endswith(".docx"):
        return extract_text(file)
    if name.endswith(".doc"):
        return extract_text(file)
    raise ValueError(f"File {name} does not have .doc or .docx extension")


def clean_text(text: str) -> str:
    """
    Nettoie le texte extrait du PDF en supprimant les caractères indésirables
    et en normalisant le format.
    """
    # Supprimer les caractères de contrôle et spéciaux sauf les retours à la ligne
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    # Remplacer les multiples espaces par un seul
    text = re.sub(r' +', ' ', text)

    # Supprimer les espaces en début et fin de ligne
    text = '\n'.join(line.strip() for line in text.split('\n'))

    # Supprimer les lignes vides multiples (garder max 2 sauts de ligne consécutifs)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Supprimer les tirets de césure en fin de ligne
    text = re.sub(r'-\n', '', text)

    # Normaliser les guillemets
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")

    # Supprimer les caractères répétés anormalement (plus de 3 fois)
    text = re.sub(r'(.)\1{3,}', r'\1\1', text)

    # Nettoyer les numéros de page isolés (optionnel)
    text = re.sub(r'\n\d+\n', '\n', text)

    # Supprimer les espaces avant la ponctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)

    # Ajouter un espace après la ponctuation si nécessaire
    text = re.sub(r'([.,;:!?])([A-Za-z])', r'\1 \2', text)

    # Trim final
    text = text.strip()

    return text


def chunk_text(text, chunk_size=500, overlap=50):
    """Divise le texte en chunks avec chevauchement"""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


