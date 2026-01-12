from rest_framework import serializers
from .models import Document, DocumentChunk
from .pdf_utils import extract_text, chunk_text, clean_text
from .embeddings import generate_embedding

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["title", "file"]

    def create(self, validated_data):
        file = validated_data["file"]
        title = validated_data.get("title") or file.name

        document = Document.objects.create(
            title=title,
            file=file,
        )

        raw_text = extract_text(file)
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

