from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
    message='Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX'
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','phone','institution','role']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, validators=[phone_validator])

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','phone','institution','role','password','password_confirm']

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Confirmação de senha não corresponde.'})
        validate_password(data.get('password'))  # usa regras do Django
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        # inicialmente bloquear até confirmação por e-mail se desejar:
        user.is_active = False
        user.save()
        return user
