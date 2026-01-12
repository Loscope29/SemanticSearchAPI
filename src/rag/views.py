
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.documents.models import DocumentChunk
from src.documents.embeddings import generate_embedding
from src.rag.utils import generate_rag_answer

# Create your views here.
class RAGAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response({"error": "Question requise"}, status=400)

        query_embedding = generate_embedding(question)

        chunks = (
            DocumentChunk.objects
            .order_by("embedding__cosine_distance", query_embedding)[:5]
        )

        context_chunks = [c.content for c in chunks]

        answer = generate_rag_answer(question, context_chunks)

        return Response({
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "document_id": c.document.id,
                    "title": c.document.title,
                    "chunk_index": c.chunk_index
                } for c in chunks
            ]
        })
