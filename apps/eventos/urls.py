from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    # Web views
    path('', views.EventListView.as_view(), name='list'),
    path('criar/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.EventUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/inscrever/', views.EnrollView.as_view(), name='enroll'),
    path('<int:pk>/cancelar/', views.CancelEnrollmentView.as_view(), name='cancel'),
    path('minhas-inscricoes/', views.MyEventsView.as_view(), name='my_events'),
    
    # API views
    path('api/', views.EventListAPIView.as_view(), name='api_list'),
    path('api/create/', views.EventCreateAPIView.as_view(), name='api_create'),
    path('api/<int:pk>/', views.EventDetailAPIView.as_view(), name='api_detail'),
    path('api/register/', views.RegisterForEventAPIView.as_view(), name='api_register'),
]
