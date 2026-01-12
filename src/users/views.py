from django.shortcuts import render
from django.views import View
from src.users.serializers import RegisterSerializer


# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import RegisterSerializer
import json

@method_decorator(csrf_exempt, name='dispatch')  # désactive temporairement CSRF pour API
class RegisterView(View):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Utilisateur créé avec succès"}, status=201)
        return JsonResponse(serializer.errors, status=400)
