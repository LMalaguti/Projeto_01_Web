from django.db import models
from usuarios.models import Usuario

class Evento(models.Model):
    TIPO_CHOICES = (
        ('seminario', 'Seminário'),
        ('palestra', 'Palestra'),
        ('minicurso', 'Minicurso'),
        ('semana', 'Semana Acadêmica'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=100)
    quantidade_participantes = models.IntegerField()
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_organizados')

    def __str__(self):
        return self.titulo

class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    certificado_emitido = models.BooleanField(default=False)

    class Meta:
        unique_together = ('evento', 'usuario')