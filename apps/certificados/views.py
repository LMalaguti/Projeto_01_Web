from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View

from .models import Certificado
from apps.audit.models import AuditLog


class CertificateListView(LoginRequiredMixin, ListView):
    """List user's certificates"""
    template_name = 'certificados/certificate_list.html'
    context_object_name = 'certificates'
    
    def get_queryset(self):
        return Certificado.objects.filter(
            user=self.request.user
        ).select_related('event').order_by('-issued_at')


class CertificateDownloadView(LoginRequiredMixin, View):
    """Download certificate file"""
    def get(self, request, pk):
        certificate = get_object_or_404(Certificado, pk=pk, user=request.user)
        
        if not certificate.file:
            raise Http404("Certificado não possui arquivo.")
        
        AuditLog.objects.create(
            user=request.user,
            action='download_certificate',
            description=f'Baixou certificado do evento: {certificate.event.title}'
        )
        
        response = FileResponse(certificate.file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="certificado_{certificate.event.id}.txt"'
        return response


# API views for backwards compatibility
from rest_framework import generics, permissions
from .serializers import CertificateSerializer


class CertificadoListAPIView(generics.ListAPIView):
    """API: List user's certificates"""
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificado.objects.filter(user=self.request.user)
