from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('criar/', views.criar_evento, name='criar'),
    path('inscricao/', views.inscricao, name='inscricao'),
]
