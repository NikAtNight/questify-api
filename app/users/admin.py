from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    User,
    UserHabit,
)


class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'email',
        'supabase_id',
        'is_active',
        'first_name',
        'last_name',
    )
    fieldsets = (
        ('Account Information', {
            'fields': (
                'id',
                'email',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
        ('Supabase Information', {
            'fields': (
                'supabase_id',
            ),
        }),
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'profile_pic',
            ),
        }),
        ('Level Information', {
            'fields': (
                'experience',
                'level',
            ),
        }),
    )
    readonly_fields = ['id']
    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = []
    list_filter = []

    ordering = ['email']


class UserHabitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'habit',
        'status',
        'start_date',
        'completion_date',
        'current_streak',
    )
    fieldsets = (
        ('User Habit Information', {
            'fields': (
                'id',
                'created_at',
                'updated_at',
                'user',
                'habit',
                'status',
                'start_date',
                'completion_date',
                'progress_percentage',
                'notifications_enabled',
            )
        }),
        ('Habit Information', {
            'fields': (
                'current_streak',
                'best_streak',
                'total_days_completed',
                'next_milestone',
                'next_skill_unlock',
            )
        }),
        ('Habit Logs', {
            'fields': (
                'habit_logs',
            )
        }),
    )
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'start_date',
        'completion_date',
    ]
    search_fields = [
        'user__email',
        'habit__name',
    ]
    list_filter = [
        'habit__category',
    ]
    ordering = [
        'user__email',
        'habit__name',
    ]
    formfield_overrides = {
        JSONField: {
            'widget': JSONEditorWidget(width='100%')
        },
    }


admin.site.register(User, UserAdmin)
admin.site.register(UserHabit, UserHabitAdmin)
