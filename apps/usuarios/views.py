from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.urls import reverse
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from .models import Usuario
from .serializers import UserSerializer, UserRegistrationSerializer

signer = TimestampSigner()

class UserRegistrationView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # gerar token assinado para confirmação (exemplo simples)
        token = signer.sign(user.pk)
        confirm_url = self.request.build_absolute_uri(
            reverse('usuarios:confirm-registration', args=[token])
        )
        # enviar email (configurar EMAIL_BACKEND em settings)
        subject = 'Confirme seu cadastro - SGEA'
        message = f'Olá {user.first_name or user.username},\n\nConfirme seu cadastro clicando no link: {confirm_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        # não ativamos aqui: a ativação será via endpoint de confirmação

class ConfirmRegistrationView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            unsigned = signer.unsign(token, max_age=60*60*24)  # 1 dia
            user = Usuario.objects.get(pk=unsigned)
            user.is_active = True
            user.save()
            return Response({'detail':'Conta confirmada.'})
        except Exception as e:
            return Response({'detail':'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
