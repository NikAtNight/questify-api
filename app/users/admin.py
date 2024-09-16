from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    list_display = ('id', 'email', 'supabase_id', 'is_active', 'first_name', 'last_name')
    fieldsets = (
        ('Account Information', {
            'fields': ('id', 'email', 'is_active', 'is_staff', 'is_superuser'),
        }),
        ('Supabase Information', {
            'fields': ('supabase_id',),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_pic'),
        }),
    )
    readonly_fields = ['id']
    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = []
    list_filter = []

    ordering = ['email']


admin.site.register(User, UserAdmin)
