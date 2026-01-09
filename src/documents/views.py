from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Document
from .serializers import DocumentSerializer
# Create your views here.

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(
        detail=True,
        methods=["get"],
        url_path="similar"
    )
    def similar(self, request, pk=None):
        return Response({
            "document_id": pk,
            "similar_documents": []
        })
