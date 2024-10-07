from django.contrib import admin

from .models import Skill


class SkillAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'points',
        'milestones',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'created_at',
                'updated_at',
                'name',
                'description',
                'points',
                'milestones',
            ),
        }),
    )
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'name',
    ]


admin.site.register(Skill, SkillAdmin)
