"""
Management command to create initial test users for SGEA.
Run with: python manage.py seed_users
"""

from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Creates initial test users for SGEA system'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'organizador',
                'email': 'organizador@sgea.com',
                'password': 'Admin@123',
                'first_name': 'Administrador',
                'last_name': 'SGEA',
                'role': 'organizador',
                'phone': '(11) 99999-0001',
                'institution': None,
                'is_staff': True,
            },
            {
                'username': 'aluno',
                'email': 'aluno@sgea.com',
                'password': 'Aluno@123',
                'first_name': 'Aluno',
                'last_name': 'Teste',
                'role': 'aluno',
                'phone': '(11) 99999-0002',
                'institution': 'Universidade Federal',
                'is_staff': False,
            },
            {
                'username': 'professor',
                'email': 'professor@sgea.com',
                'password': 'Professor@123',
                'first_name': 'Professor',
                'last_name': 'Teste',
                'role': 'professor',
                'phone': '(11) 99999-0003',
                'institution': 'Universidade Federal',
                'is_staff': False,
            },
        ]

        for user_data in users_data:
            password = user_data.pop('password')
            
            user, created = Usuario.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created user: {user.email} ({user.role})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'-> User already exists: {user.email}')
                )

        self.stdout.write(self.style.SUCCESS('\nSeed users completed!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  Organizador: organizador@sgea.com / Admin@123')
        self.stdout.write('  Aluno: aluno@sgea.com / Aluno@123')
        self.stdout.write('  Professor: professor@sgea.com / Professor@123')
