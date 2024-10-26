from django.contrib import admin

from .models import Milestone


class MilestoneAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'day',
        'points',
    )
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id',
                'created_at',
                'name',
                'day',
                'points',
            ),
        }),
    )
    readonly_fields = [
        'id',
        'created_at',
    ]
    search_fields = [
        'name',
    ]


admin.site.register(Milestone, MilestoneAdmin)
