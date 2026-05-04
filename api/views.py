from django.shortcuts import render

from api.parser.parser_vb6 import parsear_vb6
from api.parser.limpiador import limpiar_codigo
from api.parser.contexto import preparar_contexto

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TranslationSerializer

from api.ia.orquestador import OrquestadorIA
from api.Servicios.cliente_gemini import ClienteGemini


class TranslateCodeView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cliente = ClienteGemini()
        self.orquestador = OrquestadorIA(cliente)

    def post(self, request):
        
        print("FILES:", request.FILES)
        print("DATA:", request.data)
        
        file = request.FILES.get('file')


        if file:
            if not file.name.endswith(('.bas', '.frm', '.cls')):
                return Response(
                    {"error": "Formato no válido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                codigo_fuente = file.read().decode('utf-8', errors='ignore')
                lenguaje = "vb6"
            except:
                return Response(
                    {"error": "Error al leer archivo"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            serializer = TranslationSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            codigo_fuente = serializer.validated_data.get("source_code")
            lenguaje = serializer.validated_data.get("language")

        #flijo del parser
        codigo_limpio = limpiar_codigo(codigo_fuente)
        estructura = parsear_vb6(codigo_limpio)
        contexto = preparar_contexto(estructura)

        print("=== CODIGO LIMPIO ===")
        print(codigo_limpio)

        print("=== ESTRUCTURA ===")
        print(estructura)

        print("=== CONTEXTO ===")
        print(contexto)
        
        #trabajo de IA
        resultado = self.orquestador.convertir_codigo(contexto)
        print("Resultado prueba")
        print(resultado)

        return Response({
            "status": "success",
            "language": lenguaje,
            "input": codigo_fuente[:200],
            "output": resultado["codigo_convertido"]
        })
        
def home(request):
    return render(request, 'index.html')