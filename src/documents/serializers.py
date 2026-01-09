from rest_framework import serializers
from .models import Document, DocumentChunk
from .pdf_utils import extract_text_from_pdf, chunk_text, clean_text
from .embeddings import generate_embedding

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["title", "file"]

    def create(self, validated_data):
        pdf_file = validated_data["file"]

        document = Document.objects.create(**validated_data)

        raw_text = extract_text_from_pdf(pdf_file)
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text)

        for idx, chunk in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document,
                content=chunk,
                chunk_index=idx,
                embedding=generate_embedding(chunk)
            )

        return document

