from django.contrib.auth.backends import ModelBackend
from .models import Usuario


class EmailOrUsernameBackend(ModelBackend):
    """
    Authentication backend that allows login with either username or email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Usuario.USERNAME_FIELD)
        if username is None or password is None:
            return None
        
        # Try to find user by username or email
        try:
            user = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            try:
                user = Usuario.objects.get(email=username)
            except Usuario.DoesNotExist:
                # Run the default password hasher to mitigate timing attacks
                Usuario().set_password(password)
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
