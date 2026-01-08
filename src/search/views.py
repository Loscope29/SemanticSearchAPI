from rest_framework.generics import ListAPIView

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pgvector.django import CosineDistance

from documents.models import Document, DocumentChunk
from documents.embeddings import generate_embedding
from search.models import SearchQuery
from search.serializers import SearchQuerySerializer


class SemanticSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q")
        if not q:
            return Response({"error": "q requis"}, status=400)

        query_embedding = generate_embedding(q)

        chunks = (
            DocumentChunk.objects
            .annotate(
                distance=CosineDistance("embedding", query_embedding)
            )
            .order_by("distance")[:5]
        )
        # Historique utilisateur
        SearchQuery.objects.create(
            user=request.user,
            query=query_embedding
        )

        return Response([
            {
                "document": chunk.document.title,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content[:200],
                "distance": float(chunk.distance)
            }
            for chunk in chunks
        ])


class SearchHistoryAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchQuerySerializer

    def get_queryset(self):
        return (
            SearchQuery.objects
            .filter(user=self.request.user)
            .order_by("-created_at")[:10]
        )
