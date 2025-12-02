from django.db import models
from django.conf import settings

class Certificado(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    event = models.ForeignKey('eventos.Event', on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='certificates/')

    class Meta:
        unique_together = ('user','event')

    def __str__(self):
        return f'Certificado {self.user} - {self.event}'
