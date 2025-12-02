from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create_user','Criação de usuário'),
        ('create_event','Criação de evento'),
        ('update_event','Alteração de evento'),
        ('delete_event','Exclusão de evento'),
        ('api_event_list','Consulta eventos via API'),
        ('issue_certificate','Geração/consulta certificado'),
        ('registration','Inscrição evento'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.timestamp} - {self.action} - {self.user}'
