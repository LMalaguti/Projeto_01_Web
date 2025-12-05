from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView

from .models import AuditLog


class OrganizerRequiredMixin(UserPassesTestMixin):
    """Mixin that requires user to be an organizer"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'organizador'
    
    def handle_no_permission(self):
        messages.error(self.request, 'Apenas organizadores podem acessar os logs de auditoria.')
        return redirect('home')


class AuditLogListView(LoginRequiredMixin, OrganizerRequiredMixin, ListView):
    """Audit log list view (organizer only)"""
    model = AuditLog
    template_name = 'audit/audit_list.html'
    context_object_name = 'logs'
    paginate_by = 50
    ordering = ['-timestamp']
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('user')
        
        # Filter by date
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(timestamp__date=date)
        
        # Filter by user
        user_id = self.request.GET.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by action
        action = self.request.GET.get('action')
        if action:
            queryset = queryset.filter(action=action)
        
        # Search
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(description__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actions'] = AuditLog.objects.values_list('action', flat=True).distinct()
        context['selected_date'] = self.request.GET.get('date', '')
        context['selected_user'] = self.request.GET.get('user', '')
        context['selected_action'] = self.request.GET.get('action', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        from apps.usuarios.models import Usuario
        context['users'] = Usuario.objects.filter(is_active=True).order_by('first_name')
        
        return context


# API views for backwards compatibility
from rest_framework import generics, permissions
from .serializers import AuditLogSerializer


class AuditLogListAPIView(generics.ListAPIView):
    """API: List audit logs"""
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != 'organizador':
            return AuditLog.objects.none()
        return super().get_queryset()
