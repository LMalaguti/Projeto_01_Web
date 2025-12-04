"""
Management command to automatically generate certificates for completed events.
Run with: python manage.py generate_certificates

This should be run as a scheduled task (cron job) daily.
"""

import os
from io import BytesIO
from datetime import date

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import timezone

from apps.eventos.models import Event, Registration
from apps.certificados.models import Certificado
from apps.audit.models import AuditLog


class Command(BaseCommand):
    help = 'Generates certificates for participants with confirmed presence in completed events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually creating certificates',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        today = timezone.localdate()
        
        self.stdout.write(f'Checking for completed events (end_date < {today})...\n')
        
        # Find events that have ended
        completed_events = Event.objects.filter(end_date__lt=today)
        
        if not completed_events.exists():
            self.stdout.write(self.style.WARNING('No completed events found.'))
            return
        
        certificates_created = 0
        
        for event in completed_events:
            self.stdout.write(f'\nEvent: {event.title} (ended {event.end_date})')
            
            # Get registrations with confirmed presence
            confirmed_registrations = Registration.objects.filter(
                event=event,
                presence_confirmed=True
            ).select_related('user')
            
            if not confirmed_registrations.exists():
                self.stdout.write(self.style.WARNING('  -> No confirmed participants'))
                continue
            
            for registration in confirmed_registrations:
                user = registration.user
                
                # Check if certificate already exists
                if Certificado.objects.filter(user=user, event=event).exists():
                    self.stdout.write(f'  -> Certificate already exists for {user.email}')
                    continue
                
                if dry_run:
                    self.stdout.write(f'  [DRY RUN] Would create certificate for {user.email}')
                    certificates_created += 1
                    continue
                
                # Generate certificate
                try:
                    certificate = self._create_certificate(user, event)
                    certificates_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  [OK] Created certificate for {user.email}')
                    )
                    
                    # Log to audit
                    AuditLog.objects.create(
                        user=None,  # System action
                        action='issue_certificate',
                        description=f'Auto-generated certificate for {user.email} - Event: {event.title}'
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  [ERROR] Error creating certificate for {user.email}: {e}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n{"[DRY RUN] " if dry_run else ""}Completed! {certificates_created} certificates created.')
        )

    def _create_certificate(self, user, event):
        """
        Creates a certificate file and saves it to the database.
        In a production environment, this would generate a PDF.
        For now, we create a simple text-based certificate.
        """
        
        # Create certificate content (in production, use a PDF library like reportlab)
        certificate_content = f"""
================================================================================
                    CERTIFICADO DE PARTICIPAÇÃO
================================================================================

Certificamos que

                        {user.first_name} {user.last_name}

participou do evento

                        {event.title}

Tipo: {event.get_event_type_display()}
Data: {event.start_date.strftime('%d/%m/%Y')} a {event.end_date.strftime('%d/%m/%Y')}
Local: {event.location}

Professor Responsável: {event.professor_in_charge.first_name} {event.professor_in_charge.last_name}
Organizador: {event.organizer.first_name} {event.organizer.last_name}

================================================================================
            SGEA - Sistema de Gestão de Eventos Acadêmicos
                    Emitido em: {timezone.localdate().strftime('%d/%m/%Y')}
================================================================================
"""
        
        # Create the certificate record
        certificate = Certificado(
            user=user,
            event=event,
        )
        
        # Save as a text file (in production, generate PDF)
        filename = f'certificado_{event.id}_{user.id}.txt'
        certificate.file.save(filename, ContentFile(certificate_content.encode('utf-8')))
        certificate.save()
        
        return certificate
