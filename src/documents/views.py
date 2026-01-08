from django.shortcuts import render
from pgvector.django import CosineDistance
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Document, DocumentChunk
from .serializers import DocumentUploadSerializer
# Create your views here.

class PDFUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save()
        return Response({"id": doc.id, "title": doc.title})


class SimilarDocumentsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        chunk = DocumentChunk.objects.filter(document_id=id).first()

        similar = (
            DocumentChunk.objects
            .exclude(document_id=id)
            .annotate(
                distance=CosineDistance("embedding", chunk.embedding)
            )
            .order_by("distance")[:5]
        )

        return Response([
            {
                "document": c.document.title,
                "distance": float(c.distance)
            }
            for c in similar
        ])


