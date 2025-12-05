from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Web views
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.RegisterView.as_view(), name='register'),
    path('cadastro/sucesso/', views.RegisterSuccessView.as_view(), name='register_success'),
    path('confirmar/<str:token>/', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('perfil/', views.ProfileView.as_view(), name='profile'),
    
    # API views (for backwards compatibility)
    path('api/register/', views.UserRegistrationAPIView.as_view(), name='api_register'),
    path('api/confirm/<str:token>/', views.ConfirmRegistrationAPIView.as_view(), name='api_confirm'),
    path('api/me/', views.UserDetailAPIView.as_view(), name='api_me'),
]
