from rest_framework import serializers
from .models import Event, Registration
from users.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField()
    professor_in_charge = serializers.StringRelatedField()
    vacancies_left = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id','title','description','event_type','start_date','end_date','start_time','end_time','location','capacity','vacancies_left','organizer','professor_in_charge','banner']

    def get_vacancies_left(self, obj):
        return obj.vacancies_left()

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_at']

    def validate_banner(self, value):
        # valida se é imagem (Django ImageField já valida), mas asseguramos tipo
        if value and not getattr(value, 'content_type', '').startswith('image'):
            raise serializers.ValidationError('Arquivo enviado não é uma imagem.')
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Registration
        fields = ['id','user','event','registered_at','presence_confirmed']
        read_only_fields = ['registered_at','presence_confirmed']

    def validate(self, attrs):
        user = self.context['request'].user
        event = attrs.get('event')
        if event.registrations.filter(user=user).exists():
            raise serializers.ValidationError('Usuário já inscrito neste evento.')
        if event.registrations.count() >= event.capacity:
            raise serializers.ValidationError('Capacidade do evento atingida.')
        if user.role == 'organizador':
            raise serializers.ValidationError('Organizadores não podem se inscrever.')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        reg = Registration.objects.create(user=user, **validated_data)
        return reg
