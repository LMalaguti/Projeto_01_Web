from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as drf_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Import API views directly
from apps.usuarios.views import UserRegistrationAPIView, ConfirmRegistrationAPIView, UserDetailAPIView
from apps.eventos.views import EventListAPIView, EventCreateAPIView, EventDetailAPIView, RegisterForEventAPIView
from apps.certificados.views import CertificadoListAPIView
from apps.audit.views import AuditLogListAPIView

urlpatterns = [
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Web views
    path('usuarios/', include('apps.usuarios.urls')),
    path('eventos/', include('apps.eventos.urls')),
    path('certificados/', include('apps.certificados.urls')),
    path('auditoria/', include('apps.audit.urls')),
    
    # API endpoints
    path('api/token/', drf_views.obtain_auth_token, name='api-token'),
    
    # Users API
    path('api/users/register/', UserRegistrationAPIView.as_view(), name='api-user-register'),
    path('api/users/confirm/<str:token>/', ConfirmRegistrationAPIView.as_view(), name='api-user-confirm'),
    path('api/users/me/', UserDetailAPIView.as_view(), name='api-user-me'),
    
    # Events API
    path('api/events/', EventListAPIView.as_view(), name='api-event-list'),
    path('api/events/create/', EventCreateAPIView.as_view(), name='api-event-create'),
    path('api/events/<int:pk>/', EventDetailAPIView.as_view(), name='api-event-detail'),
    path('api/events/register/', RegisterForEventAPIView.as_view(), name='api-event-register'),
    
    # Certificates API
    path('api/certificates/', CertificadoListAPIView.as_view(), name='api-certificate-list'),
    
    # Audit API
    path('api/audit/', AuditLogListAPIView.as_view(), name='api-audit-list'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)