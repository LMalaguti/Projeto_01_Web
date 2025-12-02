from rest_framework import generics, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class AuditListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user__username','action','timestamp']
    ordering_fields = ['timestamp']
