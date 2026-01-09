from django.urls import path
from .views import PDFUploadAPIView, SimilarDocumentsAPIView

urlpatterns = [
    path('', PDFUploadAPIView.as_view(), name='document-upload'),
    path('<int:id>/similar/', SimilarDocumentsAPIView.as_view(), name='similar-documents'),
]