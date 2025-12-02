from rest_framework import generics, permissions
from .models import Certificado
from .serializers import CertificateSerializer
from apps.audit.models import AuditLog

class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # alunos e professores veem apenas os próprios certificados
        user = self.request.user
        if user.role in ('aluno','professor'):
            return Certificado.objects.filter(user=user)
        # organizador pode ver todos
        return Certificado.objects.all()

    def list(self, request, *args, **kwargs):
        AuditLog.objects.create(user=request.user, action='issue_certificate', description='Consultou certificados')
        return super().list(request, *args, **kwargs)
