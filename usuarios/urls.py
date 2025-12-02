from django.urls import path
from .views import UserRegistrationView, ConfirmRegistrationView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('confirm/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm-registration'),
    path('me/', UserDetailView.as_view(), name='me'),  # pode ser ajustado para usar request.user
]
