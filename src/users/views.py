from django.shortcuts import render
from rest_framework import viewsets

from documents import models


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

