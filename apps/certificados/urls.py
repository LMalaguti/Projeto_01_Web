from django.urls import path
from . import views

app_name = 'certificados'

urlpatterns = [
    # Web views
    path('', views.CertificateListView.as_view(), name='list'),
    path('<int:pk>/download/', views.CertificateDownloadView.as_view(), name='download'),
    
    # API views
    path('api/', views.CertificadoListAPIView.as_view(), name='api_list'),
]
