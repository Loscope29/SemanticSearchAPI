from django.urls import path
from rest_framework import routers
from .views import PDFUploadAPIView, SimilarDocumentsAPIView

router = routers.SimpleRouter()
router.register("", PDFUploadAPIView, basename="documents")

urlpatterns = [
    path("<int:id>/similar/", SimilarDocumentsAPIView.as_view()),
]
