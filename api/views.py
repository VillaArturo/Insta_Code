from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from .serializers import TranslationSerializer
from .models import Traduccion

from api.parser.parser_vb6 import parsear_vb6
from api.parser.limpiador import limpiar_codigo
from api.parser.contexto import preparar_contexto
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
            if not file.name.endswith(('.bas', '.frm', '.cls', '.vb')):
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

        codigo_limpio = limpiar_codigo(codigo_fuente)
        estructura = parsear_vb6(codigo_limpio)
        contexto = preparar_contexto(estructura)

        print("=== CODIGO LIMPIO ===")
        print(codigo_limpio)
        print("=== ESTRUCTURA ===")
        print(estructura)
        print("=== CONTEXTO ===")
        print(contexto)

        resultado = self.orquestador.convertir_codigo(contexto)
        print("Resultado prueba")
        print(resultado)

        if request.user.is_authenticated:
            print("=== GUARDANDO TRADUCCION ===")
            print("Usuario:", request.user)
            Traduccion.objects.create(
                usuario=request.user,
                archivo=file.name if file else "texto directo",
                codigo_original=codigo_fuente,
                codigo_traducido=resultado["codigo_convertido"]
            )
        else:
            print("=== USUARIO NO AUTENTICADO ===")

        return Response({
            "status": "success",
            "language": lenguaje,
            "input": codigo_fuente[:200],
            "output": resultado["codigo_convertido"]
        })


def home(request):
    return render(request, 'index.html')


def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error = "Usuario o contraseña incorrectos"
    return render(request, "registrar/login.html", {"error": error, "form": "login"})


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            error = "Ese usuario ya existe"
            return render(request, "registrar/login.html", {"error": error, "form": "register"})
        User.objects.create_user(username=username, email=email, password=password)
        return redirect("login")
    return render(request, "registrar/login.html", {"error": error, "form": "register"})


@login_required(login_url='/login/')
def historial_view(request):
    traducciones = Traduccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'registrar/historial.html', {'traducciones': traducciones})