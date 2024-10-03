from django.db import models
import uuid


class Skill(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    skill_name = models.CharField(
        max_length=255
    )
    description = models.TextField()
    category = models.CharField(
        max_length=100,
        choices=[
            ('Health', 'Health'),
            ('Productivity', 'Productivity'),
            ('Learning', 'Learning'),
        ]
    )
    reward_points = models.IntegerField(
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.skill_name
