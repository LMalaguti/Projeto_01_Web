from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('eventos/', include('eventos.urls', namespace='eventos')),
    path('certificados/', include('certificados.urls', namespace='certificados')),
]
