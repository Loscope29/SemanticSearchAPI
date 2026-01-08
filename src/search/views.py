from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pgvector.django import CosineDistance

from documents.models import Document
from documents.services import generate_embedding
from search.models import SearchQuery


class SemanticSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response(
                {"error": "Le paramètre q est requis"},
                status=400
            )

        # Embedding de la requête
        query_embedding = generate_embedding(query)

        # Recherche vectorielle en base (pgvector)
        documents = (
            Document.objects
            .annotate(
                distance=CosineDistance("embedding", query_embedding)
            )
            .order_by("distance")[:5]
        )

        # Historique utilisateur
        SearchQuery.objects.create(
            user=request.user,
            query=query
        )

        # Réponse API
        results = []
        for doc in documents:
            results.append({
                "id": doc.id,
                "title": doc.title,
                "distance": float(doc.distance),
            })

        return Response(results, status=200)

class SearchHistoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchQuerySerializer

    def get_queryset(self):
        return (
            SearchQuery.objects
            .filter(user=self.request.user)
            .order_by("-created_at")[:10]
        )
