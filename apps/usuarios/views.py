from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from .models import Usuario
from .forms import LoginForm, UserRegistrationForm, UserProfileForm
from apps.audit.models import AuditLog

signer = TimestampSigner()


class LoginView(BaseLoginView):
    """User login view"""
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, f'Bem-vindo(a), {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)


class LogoutView(View):
    """User logout view"""
    def get(self, request):
        logout(request)
        messages.info(request, 'Você saiu do sistema.')
        return redirect('home')
    
    def post(self, request):
        return self.get(request)


class RegisterView(CreateView):
    """User registration view"""
    template_name = 'usuarios/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('usuarios:register_success')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        
        # Generate confirmation token
        token = signer.sign(user.pk)
        confirm_url = self.request.build_absolute_uri(
            reverse('usuarios:confirm_email', args=[token])
        )
        
        # Send confirmation email
        subject = 'Confirme seu cadastro - SGEA'
        message = f'''Olá {user.first_name or user.username},

Obrigado por se cadastrar no SGEA - Sistema de Gestão de Eventos Acadêmicos!

Para ativar sua conta, clique no link abaixo:
{confirm_url}

Este link expira em 24 horas.

Se você não solicitou este cadastro, ignore este e-mail.

Atenciosamente,
Equipe SGEA
'''
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        except Exception as e:
            # Log error but don't fail registration
            print(f"Email error: {e}")
        
        # Log to audit
        AuditLog.objects.create(
            user=None,
            action='create_user',
            description=f'Novo usuário registrado: {user.email} ({user.role})'
        )
        
        return super().form_valid(form)


class RegisterSuccessView(TemplateView):
    """Registration success page"""
    template_name = 'usuarios/register_success.html'


class ConfirmEmailView(View):
    """Email confirmation view"""
    def get(self, request, token):
        try:
            user_pk = signer.unsign(token, max_age=60*60*24)  # 24 hours
            user = get_object_or_404(Usuario, pk=user_pk)
            
            if user.is_active:
                messages.info(request, 'Sua conta já foi confirmada anteriormente.')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Conta confirmada com sucesso! Você já pode fazer login.')
                
                AuditLog.objects.create(
                    user=user,
                    action='create_user',
                    description=f'Usuário confirmou e-mail: {user.email}'
                )
            
            return redirect('usuarios:login')
            
        except SignatureExpired:
            messages.error(request, 'O link de confirmação expirou. Por favor, registre-se novamente.')
            return redirect('usuarios:register')
        except BadSignature:
            messages.error(request, 'Link de confirmação inválido.')
            return redirect('home')


class ProfileView(LoginRequiredMixin, UpdateView):
    """User profile view and edit"""
    template_name = 'usuarios/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('usuarios:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


# Keep API views for backwards compatibility
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegistrationSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """API: User registration"""
    queryset = Usuario.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = signer.sign(user.pk)
        confirm_url = self.request.build_absolute_uri(
            reverse('usuarios:confirm_email', args=[token])
        )
        subject = 'Confirme seu cadastro - SGEA'
        message = f'Olá {user.first_name or user.username},\n\nConfirme seu cadastro clicando no link: {confirm_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


class ConfirmRegistrationAPIView(generics.GenericAPIView):
    """API: Email confirmation"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            unsigned = signer.unsign(token, max_age=60*60*24)
            user = Usuario.objects.get(pk=unsigned)
            user.is_active = True
            user.save()
            return Response({'detail': 'Conta confirmada.'})
        except Exception:
            return Response({'detail': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveAPIView):
    """API: Get current user details"""
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
