from django.db.models import Q
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from .models import Document
from .serializers import DocumentSerializer
# Create your views here.

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class SimilarDocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('content',)

    def get_queryset(self):
        queryset = Document.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            return queryset
        return queryset

