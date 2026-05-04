from django.db import models
from django.contrib.auth.models import User

class Traduccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='traducciones')
    archivo = models.CharField(max_length=255, blank=True)
    codigo_original = models.TextField()
    codigo_traducido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.archivo} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"