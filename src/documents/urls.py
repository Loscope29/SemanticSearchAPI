from django.urls import path
from rest_framework import routers
from .views import DocumentViewSet

router = routers.SimpleRouter()
router.register("", DocumentViewSet, basename="documents")

urlpatterns = [
    path("<int:id>/similar/", SimilarDocumentsAPIView.as_view()),
]
