from django.urls import path

from src.rag.views import RAGAPIView

urlpatterns = [
    path('ask/', RAGAPIView.as_view(), name= 'ask'),
]