import uuid
from django.db import models


class Habit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    name = models.CharField(
        max_length=255
    )
    category = models.ManyToManyField(
        'external.Category',
        related_name='habits',
    )
    difficulty_level = models.CharField(
        max_length=50,
        choices=[
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
        ]
    )
    milestones = models.JSONField(
        default=list,
        blank=True
    )
    skills = models.ManyToManyField(
        'skills.Skill',
        related_name='habits',
    )
    experience = models.FloatField(
        default=0.0
    )

    def __str__(self):
        return self.name
