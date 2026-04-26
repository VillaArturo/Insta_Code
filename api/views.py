from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TranslationSerializer

from api.ia.orquestador import OrquestadorIA


class TranslateCodeView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orquestador = OrquestadorIA()

    def post(self, request):
        serializer = TranslationSerializer(data=request.data)

        if serializer.is_valid():
            # Datos correctos según tu serializer
            codigo_fuente = serializer.validated_data.get("source_code")
            lenguaje = serializer.validated_data.get("language")

            # Aquí entra la IA
            resultado = self.orquestador.convertir_codigo(codigo_fuente)

            return Response({
                "status": "success",
                "language": lenguaje,
                "input": codigo_fuente,
                "output": resultado["codigo_convertido"]
            })

        return Response(serializer.errors, status=400)