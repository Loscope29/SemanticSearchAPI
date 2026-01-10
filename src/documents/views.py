from pgvector.django import CosineDistance
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=['get'], url_path='similar', permission_classes=[IsAuthenticated])
    def similar(self, request, pk=None):
        """
        Trouve les 5 documents les plus similaires basés sur les embeddings.

        GET /api/documents/{id}/similar/
        """
        try:
            document = self.get_object()

            # Vérifier que le document a un embedding
            if not document.embedding:
                return Response(
                    {'error': 'Le document n\'a pas d\'embedding'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Récupérer les documents similaires
            similar_docs = (
                Document.objects
                .exclude(id=document.id)
                .annotate(
                    distance=CosineDistance("embedding", document.embedding)
                )
                .order_by("distance")[:5]
            )

            return Response([
                {
                    "id": doc.id,
                    "title": doc.title,
                    "distance": float(doc.distance)
                }
                for doc in similar_docs
            ])

        except Document.DoesNotExist:
            return Response(
                {'error': 'Document non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
