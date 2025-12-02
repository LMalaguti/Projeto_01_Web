from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario

@admin.register(Usuario)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra', {'fields': ('phone','institution','role')}),
    )
    list_display = ('username','email','role','is_active')
