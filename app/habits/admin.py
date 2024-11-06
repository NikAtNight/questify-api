from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    Habit,
    UserHabit,
    HabitLog,
)


class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'difficulty_level',
        'experience',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'created_at',
                'name',
                'difficulty_level',
                'experience',
            ),
        }),
        ('Category', {
            'fields': (
                'category',
            ),
        }),
        ('Milestones', {
            'fields': (
                'milestones',
            ),
        }),
    )
    filter_horizontal = [
        'milestones',
        'category',
    ]
    readonly_fields = [
        'id',
        'created_at',
    ]
    list_filter = [
        'difficulty_level',
    ]
    search_fields = [
        'name',
    ]
    formfield_overrides = {
        JSONField: {
            'widget': JSONEditorWidget(width='100%')
        },
    }


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
            )
        }),
        ('Habit Information', {
            'fields': (
                'current_streak',
                'best_streak',
                'total_days_completed',
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


class HabitLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'habit',
        'created_at',
    )
    search_fields = [
        'user__email',
        'habit__name',
    ]
    list_filter = [
        'created_at',
    ]
    ordering = [
        'user__email',
        'habit__name',
    ]


admin.site.register(Habit, HabitAdmin)
admin.site.register(UserHabit, UserHabitAdmin)
admin.site.register(HabitLog, HabitLogAdmin)
