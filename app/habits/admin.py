from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from .models import Habit


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
        ('Skills', {
            'fields': (
                'skills',
            ),
        }),
    )
    filter_horizontal = [
        'skills',
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


admin.site.register(Habit, HabitAdmin)
