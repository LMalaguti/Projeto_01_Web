from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    PERFIL_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('organizador', 'Organizador'),
    )
    telefone = models.CharField(max_length=15)
    instituicao = models.CharField(max_length=100, blank=True, null=True)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES)

    def __str__(self):
        return self.username