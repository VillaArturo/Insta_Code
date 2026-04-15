from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TranslationSerializer

class TranslateCodeView(APIView):
    def post(self, request):
        serializer = TranslationSerializer(data=request.data)
        if serializer.is_valid():
            # Aquí irá la magia de Inta_Code después
            return Response({"message": "API conectada", "status": "ready"})
        return Response(serializer.errors, status=400)
