from django import forms
from django.utils import timezone
from .models import Event, Registration
from apps.usuarios.models import Usuario


class EventForm(forms.ModelForm):
    """Form for creating and editing events"""
    
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'start_date', 'end_date',
            'start_time', 'end_time', 'location', 'capacity', 'professor_in_charge', 'banner'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do evento'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o evento...'
            }),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Local do evento'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Número de vagas'
            }),
            'professor_in_charge': forms.Select(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'event_type': 'Tipo de Evento',
            'start_date': 'Data de Início',
            'end_date': 'Data de Término',
            'start_time': 'Horário de Início',
            'end_time': 'Horário de Término',
            'location': 'Local',
            'capacity': 'Número de Vagas',
            'professor_in_charge': 'Professor Responsável',
            'banner': 'Banner do Evento',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter professors only
        self.fields['professor_in_charge'].queryset = Usuario.objects.filter(
            role='professor', is_active=True
        )

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.localdate():
            raise forms.ValidationError('A data de início não pode ser anterior a hoje.')
        return start_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'A data de término não pode ser anterior à data de início.')

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date == end_date and start_time and end_time:
            if end_time < start_time:
                self.add_error('end_time', 'O horário de término não pode ser anterior ao horário de início.')
        
        # Validate banner is an image
        banner = cleaned_data.get('banner')
        if banner and hasattr(banner, 'content_type'):
            if not banner.content_type.startswith('image'):
                self.add_error('banner', 'O arquivo deve ser uma imagem.')
        
        return cleaned_data


class RegistrationForm(forms.Form):
    """Form for event registration"""
    event_id = forms.IntegerField(widget=forms.HiddenInput())
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean(self):
        cleaned_data = super().clean()
        event_id = cleaned_data.get('event_id')
        
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise forms.ValidationError('Evento não encontrado.')
        
        # Check if already registered
        if Registration.objects.filter(user=self.user, event=event).exists():
            raise forms.ValidationError('Você já está inscrito neste evento.')
        
        # Check capacity
        if event.registrations.count() >= event.capacity:
            raise forms.ValidationError('Este evento atingiu a capacidade máxima.')
        
        # Check if organizer
        if self.user.role == 'organizador':
            raise forms.ValidationError('Organizadores não podem se inscrever em eventos.')
        
        cleaned_data['event'] = event
        return cleaned_data