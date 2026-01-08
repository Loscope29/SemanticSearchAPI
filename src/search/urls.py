from django.urls import path
from .views import SemanticSearchAPIView

urlpatterns = [
    path("semantic/", SemanticSearchAPIView.as_view()),
    path("history/", SearchHistoryAPIView.as_view()),
]
