from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    # Web views
    path('', views.AuditLogListView.as_view(), name='list'),
    
    # API views
    path('api/', views.AuditLogListAPIView.as_view(), name='api_list'),
]
