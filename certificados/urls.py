from django.urls import path
from . import views

app_name = 'certificados'

urlpatterns = [
    path('gerar/', views.gerar_certificado, name='gerar'),
]
