from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as drf_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

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
    path('api/users/', include('apps.usuarios.urls', namespace='api_usuarios')),
    path('api/events/', include('apps.eventos.urls', namespace='api_eventos')),
    path('api/certificates/', include('apps.certificados.urls', namespace='api_certificados')),
    path('api/audit/', include('apps.audit.urls', namespace='api_audit')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)