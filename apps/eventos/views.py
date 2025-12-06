from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from .models import Event, Registration
from .forms import EventForm
from apps.audit.models import AuditLog


class OrganizerRequiredMixin(UserPassesTestMixin):
    """Mixin that requires user to be an organizer"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'organizador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'Apenas organizadores podem realizar esta ação.')
        return redirect('eventos:list')


class EventListView(ListView):
    """List all events"""
    model = Event
    template_name = 'eventos/event_list.html'
    context_object_name = 'events'
    ordering = ['start_date']
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by event type
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Search
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.EVENT_TYPES
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class EventDetailView(DetailView):
    """Event detail page with enrollment option"""
    model = Event
    template_name = 'eventos/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user
        
        context['is_enrolled'] = False
        context['can_enroll'] = False
        
        if user.is_authenticated:
            context['is_enrolled'] = Registration.objects.filter(user=user, event=event).exists()
            context['can_enroll'] = (
                user.role != 'organizador' and 
                not context['is_enrolled'] and 
                event.vacancies_left() > 0
            )
        
        context['registrations'] = event.registrations.select_related('user').order_by('-registered_at')[:10]
        return context


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    """Create new event (organizer only)"""
    model = Event
    form_class = EventForm
    template_name = 'eventos/event_form.html'
    success_url = reverse_lazy('eventos:list')
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        response = super().form_valid(form)
        
        AuditLog.objects.create(
            user=self.request.user,
            action='create_event',
            description=f'Criou evento: {self.object.title}'
        )
        
        messages.success(self.request, f'Evento "{self.object.title}" criado com sucesso!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar Evento'
        context['button_text'] = 'Criar Evento'
        return context


class EventUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    """Edit event (organizer only)"""
    model = Event
    form_class = EventForm
    template_name = 'eventos/event_form.html'
    
    def get_success_url(self):
        return reverse_lazy('eventos:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        AuditLog.objects.create(
            user=self.request.user,
            action='update_event',
            description=f'Editou evento: {self.object.title}'
        )
        
        messages.success(self.request, f'Evento "{self.object.title}" atualizado com sucesso!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Evento'
        context['button_text'] = 'Salvar Alterações'
        return context


class EventDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    """Delete event (organizer only)"""
    model = Event
    template_name = 'eventos/event_confirm_delete.html'
    success_url = reverse_lazy('eventos:list')
    
    def form_valid(self, form):
        event_title = self.object.title
        
        AuditLog.objects.create(
            user=self.request.user,
            action='delete_event',
            description=f'Excluiu evento: {event_title}'
        )
        
        response = super().form_valid(form)
        messages.success(self.request, f'Evento "{event_title}" excluído com sucesso!')
        return response


class EnrollView(LoginRequiredMixin, View):
    """Enroll in an event"""
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        user = request.user
        
        # Validate enrollment
        if user.role == 'organizador':
            messages.error(request, 'Organizadores não podem se inscrever em eventos.')
            return redirect('eventos:detail', pk=pk)
        
        if Registration.objects.filter(user=user, event=event).exists():
            messages.warning(request, 'Você já está inscrito neste evento.')
            return redirect('eventos:detail', pk=pk)
        
        if event.vacancies_left() <= 0:
            messages.error(request, 'Este evento atingiu a capacidade máxima.')
            return redirect('eventos:detail', pk=pk)
        
        # Create registration
        Registration.objects.create(user=user, event=event)
        
        AuditLog.objects.create(
            user=user,
            action='registration',
            description=f'Inscreveu-se no evento: {event.title}'
        )
        
        messages.success(request, f'Inscrição no evento "{event.title}" realizada com sucesso!')
        return redirect('eventos:detail', pk=pk)


class CancelEnrollmentView(LoginRequiredMixin, View):
    """Cancel enrollment in an event"""
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        registration = get_object_or_404(Registration, user=request.user, event=event)
        
        registration.delete()
        
        AuditLog.objects.create(
            user=request.user,
            action='registration',
            description=f'Cancelou inscrição no evento: {event.title}'
        )
        
        messages.info(request, f'Inscrição no evento "{event.title}" cancelada.')
        return redirect('eventos:detail', pk=pk)


class MyEventsView(LoginRequiredMixin, ListView):
    """List user's enrolled events"""
    template_name = 'eventos/my_events.html'
    context_object_name = 'registrations'
    
    def get_queryset(self):
        return Registration.objects.filter(
            user=self.request.user
        ).select_related('event').order_by('-registered_at')


class DemoEndEventView(LoginRequiredMixin, OrganizerRequiredMixin, View):
    """
    Demo view: Ends an event, confirms all registrations, and generates certificates.
    This is for presentation/demo purposes only.
    """
    def post(self, request, pk):
        from datetime import date, timedelta
        from django.utils import timezone
        from django.core.files.base import ContentFile
        from apps.certificados.models import Certificado
        
        event = get_object_or_404(Event, pk=pk)
        
        # Step 1: End the event (set end_date to yesterday)
        event.end_date = date.today() - timedelta(days=1)
        if event.start_date > event.end_date:
            event.start_date = event.end_date
        event.save()
        
        # Step 2: Confirm presence for all registrations
        registrations = Registration.objects.filter(event=event)
        confirmed_count = registrations.update(presence_confirmed=True)
        
        # Step 3: Generate certificates for all confirmed participants
        certificates_created = 0
        for registration in registrations.select_related('user'):
            user = registration.user
            
            # Skip if certificate already exists
            if Certificado.objects.filter(user=user, event=event).exists():
                continue
            
            # Generate certificate
            certificate_content = f"""
================================================================================
                    CERTIFICADO DE PARTICIPAÇÃO
================================================================================

Certificamos que

                        {user.get_full_name() or user.username}

participou do evento

                        {event.title}

Tipo: {event.get_event_type_display()}
Data: {event.start_date.strftime('%d/%m/%Y')} a {event.end_date.strftime('%d/%m/%Y')}
Local: {event.location}

Professor Responsável: {event.professor_in_charge.get_full_name() or event.professor_in_charge.username}
Organizador: {event.organizer.get_full_name() or event.organizer.username}

================================================================================
            SGEA - Sistema de Gestão de Eventos Acadêmicos
                    Emitido em: {timezone.localdate().strftime('%d/%m/%Y')}
================================================================================
"""
            certificate = Certificado(user=user, event=event)
            filename = f'certificado_{event.id}_{user.id}.txt'
            certificate.file.save(filename, ContentFile(certificate_content.encode('utf-8')))
            certificate.save()
            certificates_created += 1
        
        # Log the demo action
        AuditLog.objects.create(
            user=request.user,
            action='demo_end_event',
            description=f'[DEMO] Finalizou evento "{event.title}", confirmou {confirmed_count} presenças, gerou {certificates_created} certificados'
        )
        
        messages.success(
            request, 
            f'✅ Demo: Evento finalizado! {confirmed_count} presenças confirmadas, {certificates_created} certificados gerados.'
        )
        return redirect('eventos:detail', pk=pk)


# API Views for backwards compatibility
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import EventSerializer, EventCreateSerializer, RegistrationSerializer
from .throttles import EventListThrottle, RegistrationThrottle


class EventListAPIView(generics.ListAPIView):
    """API: List events"""
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [EventListThrottle]

    def list(self, request, *args, **kwargs):
        AuditLog.objects.create(user=request.user, action='api_event_list', description='Listou eventos via API')
        return super().list(request, *args, **kwargs)


class EventCreateAPIView(generics.CreateAPIView):
    """API: Create event"""
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'organizador':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Apenas organizadores podem criar eventos.')
        serializer.save(organizer=user)
        AuditLog.objects.create(user=user, action='create_event', description=f'Criou evento via API: {serializer.instance.id}')


class EventDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API: Event detail/update/delete"""
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterForEventAPIView(generics.CreateAPIView):
    """API: Register for event"""
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [RegistrationThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        AuditLog.objects.create(user=request.user, action='registration', description=f'Inscreveu-se via API no evento {serializer.instance.event.id}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
