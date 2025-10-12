from django.db import models
from eventos.models import Inscricao

class Certificado(models.Model):
    inscricao = models.OneToOneField(Inscricao, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='certificados/')
    data_emissao = models.DateTimeField(auto_now_add=True)