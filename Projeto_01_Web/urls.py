from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as drf_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/token/', drf_views.obtain_auth_token, name='api-token'),
    path('api/users/', include('apps.usuarios.urls')),
    path('api/events/', include('apps.eventos.urls')),
    path('api/certificates/', include('apps.certificados.urls')),
    path('api/audit/', include('apps.audit.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)