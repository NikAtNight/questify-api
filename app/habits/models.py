import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField


class Habit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255
    )
    category = models.CharField(
        max_length=100,
        choices=[
            ('Health', 'Health'),
            ('Productivity', 'Productivity'),
            ('Learning', 'Learning'),
            # Add more categories as needed
        ]
    )
    difficulty_level = models.CharField(
        max_length=50,
        choices=[
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
        ]
    )
    milestones = JSONField()
    skills = models.ManyToManyField(
        'skills.Skill',
        related_name='habits'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
