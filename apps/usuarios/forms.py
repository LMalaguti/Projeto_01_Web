from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from .models import Usuario


phone_validator = RegexValidator(
    regex=r'^\(\d{2}\)\s?\d{4,5}-?\d{4}$',
    message='Telefone deve estar no formato (XX) XXXXX-XXXX'
)


class LoginForm(AuthenticationForm):
    """Custom login form with styled fields"""
    username = forms.CharField(
        label='Usuário ou E-mail',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário ou e-mail',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class UserRegistrationForm(forms.ModelForm):
    """User registration form with password confirmation"""
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mínimo 8 caracteres com letras, números e símbolos'
        }),
        help_text='Mínimo 8 caracteres, incluindo letras, números e caracteres especiais'
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha novamente'
        })
    )
    phone = forms.CharField(
        label='Telefone',
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-mask',
            'placeholder': '(XX) XXXXX-XXXX'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'institution', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da instituição'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'institution': 'Instituição',
            'role': 'Perfil',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', 'As senhas não coincidem.')
            
            # Validate password strength
            if len(password) < 8:
                self.add_error('password', 'A senha deve ter no mínimo 8 caracteres.')
            if not any(c.isalpha() for c in password):
                self.add_error('password', 'A senha deve conter letras.')
            if not any(c.isdigit() for c in password):
                self.add_error('password', 'A senha deve conter números.')
            if not any(c in '!@#$%^&*(),.?":{}|<>' for c in password):
                self.add_error('password', 'A senha deve conter caracteres especiais.')

        # Institution required for aluno and professor
        role = cleaned_data.get('role')
        institution = cleaned_data.get('institution')
        if role in ('aluno', 'professor') and not institution:
            self.add_error('institution', 'Instituição é obrigatória para alunos e professores.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False  # Inactive until email confirmation
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    phone = forms.CharField(
        label='Telefone',
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-mask',
            'placeholder': '(XX) XXXXX-XXXX'
        })
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'phone', 'institution']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'institution': 'Instituição',
        }
