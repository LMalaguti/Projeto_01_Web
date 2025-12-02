from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class Usuario(AbstractUser):
    ROLE_ALUNO = 'aluno'
    ROLE_PROFESSOR = 'professor'
    ROLE_ORGANIZADOR = 'organizador'
    ROLE_CHOICES = (
        (ROLE_ALUNO, 'Aluno'),
        (ROLE_PROFESSOR, 'Professor'),
        (ROLE_ORGANIZADOR, 'Organizador'),
    )

    phone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    institution = models.CharField('Instituição', max_length=255, blank=True, null=True)
    role = models.CharField('Perfil', max_length=20, choices=ROLE_CHOICES)

    def clean(self):
        # instituição obrigatória para aluno e professor
        if self.role in (self.ROLE_ALUNO, self.ROLE_PROFESSOR) and not self.institution:
            raise ValidationError('Instituição é obrigatória para alunos e professores.')

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
