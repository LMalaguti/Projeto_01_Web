from rest_framework import generics, permissions, status
from .models import Event
from .serializers import EventSerializer, EventCreateSerializer, RegistrationSerializer
from .throttles import EventListThrottle, RegistrationThrottle
from rest_framework.response import Response
from apps.audit.models import AuditLog

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('start_date')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [EventListThrottle]

    def list(self, request, *args, **kwargs):
        # registrar auditoria
        AuditLog.objects.create(user=request.user, action='api_event_list', description='Listou eventos via API')
        return super().list(request, *args, **kwargs)

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # validar se organizador é o mesmo ou se o usuário tem permissão
        user = self.request.user
        if user.role != 'organizador':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Apenas organizadores podem criar eventos.')
        serializer.save(organizer=user)
        AuditLog.objects.create(user=user, action='create_event', description=f'Criou evento {serializer.instance.id}')

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
        AuditLog.objects.create(user=self.request.user, action='update_event', description=f'Alterou evento {serializer.instance.id}')

    def perform_destroy(self, instance):
        eid = instance.id
        instance.delete()
        AuditLog.objects.create(user=self.request.user, action='delete_event', description=f'Excluiu evento {eid}')

class RegisterForEventView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [RegistrationThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        AuditLog.objects.create(user=request.user, action='registration', description=f'Inscreveu-se no evento {serializer.instance.event.id}')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
