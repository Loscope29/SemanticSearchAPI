from django.urls import path
from .views import DocumentUploadAPIView, SimilarDocumentsAPIView


urlpatterns = [
    path("", DocumentUploadAPIView.as_view(), name= 'upload'),
    path("<int:id>/similar/", SimilarDocumentsAPIView.as_view(), name= 'similar'),
]
