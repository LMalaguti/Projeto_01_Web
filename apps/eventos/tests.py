from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Event
from apps.usuarios.models import Usuario
import datetime

class EventValidationTests(TestCase):
    def setUp(self):
        # Create a user to be the organizer and professor
        self.user = Usuario.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='password123',
            role='professor',
            institution='Test University'
        )

    def test_end_time_before_start_time_same_day(self):
        """Test that an event cannot end before it starts on the same day"""
        today = timezone.now().date()
        future_date = today + datetime.timedelta(days=10)
        
        event = Event(
            title="Invalid Event",
            event_type="workshop",
            start_date=future_date,
            end_date=future_date, # Same day
            start_time=datetime.time(14, 0), # 14:00
            end_time=datetime.time(13, 0),   # 13:00 (Before start)
            location="Room 101",
            capacity=10,
            organizer=self.user,
            professor_in_charge=self.user
        )
        
        
        with self.assertRaises(ValidationError) as context: # Expecting ValidationError
            event.full_clean()
        
        self.assertTrue('Data final não pode ser anterior' in str(context.exception) or 'Horário' in str(context.exception))

    def test_valid_event_same_day(self):
        """Test that an event with valid time on same day passes"""
        today = timezone.now().date()
        future_date = today + datetime.timedelta(days=10)
        
        event = Event(
            title="Valid Event",
            event_type="workshop",
            start_date=future_date,
            end_date=future_date,
            start_time=datetime.time(13, 0),
            end_time=datetime.time(14, 0),
            location="Room 101",
            capacity=10,
            organizer=self.user,
            professor_in_charge=self.user
        )
        event.full_clean() # Should not raise


