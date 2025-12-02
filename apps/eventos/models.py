from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    EVENT_TYPES = (
        ('seminario','Seminário'),
        ('palestra','Palestra'),
        ('workshop','Workshop'),
        ('curso','Curso'),
    )

    title = models.CharField('Título', max_length=255)
    description = models.TextField('Descrição', blank=True)
    event_type = models.CharField('Tipo', max_length=50, choices=EVENT_TYPES)
    start_date = models.DateField('Data início')
    end_date = models.DateField('Data fim')
    start_time = models.TimeField('Horário início', null=True, blank=True)
    end_time = models.TimeField('Horário fim', null=True, blank=True)
    location = models.CharField('Local', max_length=255)
    capacity = models.PositiveIntegerField('Vagas')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='organized_events')
    professor_in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='events_as_professor')
    banner = models.ImageField('Banner', upload_to='banners/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_date < timezone.localdate():
            raise ValidationError('Data de início não pode ser anterior à data atual.')
        if self.end_date < self.start_date:
            raise ValidationError('Data final não pode ser anterior à data inicial.')
        # garantir professor
        if not self.professor_in_charge:
            raise ValidationError('Evento deve ter um professor responsável.')

    def vacancies_left(self):
        return max(0, self.capacity - self.registrations.count())

    def __str__(self):
        return f'{self.title} ({self.start_date})'

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    presence_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','event')
        ordering = ['-registered_at']

    def clean(self):
        # proibir organizer de se inscrever
        if self.user.role == getattr(settings, 'ORGANIZER_ROLE', 'organizador'):
            raise ValidationError('Organizadores não podem se inscrever em eventos.')
        # capacidade
        if self.pk is None and self.event.registrations.count() >= self.event.capacity:
            raise ValidationError('Capacidade do evento atingida.')