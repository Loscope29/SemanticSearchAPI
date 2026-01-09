from django.urls import path
from rest_framework import routers
from .views import DocumentViewSet, SimilarDocumentViewSet

router = routers.SimpleRouter()
router.register("", DocumentViewSet, basename="documents")

urlpatterns = router.urls


