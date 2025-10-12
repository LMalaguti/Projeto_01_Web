from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['tipo', 'titulo', 'descricao', 'data_inicio', 'data_fim', 'horario', 'local', 'quantidade_participantes']