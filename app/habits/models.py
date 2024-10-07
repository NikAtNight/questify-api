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


class UserHabit(models.Model):
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
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    habit = models.ForeignKey(
        'habits.Habit',
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True
    )
    completion_date = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('Not Started', 'Not Started'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            ('Abandoned', 'Abandoned'),
        ]
    )
    current_streak = models.IntegerField(
        default=0
    )
    best_streak = models.IntegerField(
        default=0
    )
    total_days_completed = models.IntegerField(
        default=0
    )
    next_milestone = models.IntegerField(
        default=0
    )
    next_skill_unlock = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    progress_percentage = models.FloatField(
        default=0.0
    )
    notifications_enabled = models.BooleanField(
        default=True
    )
    habit_logs = models.JSONField(
        default=list,
        blank=True
    )

    def __str__(self):
        return f'{self.user.email} - {self.habit.name}'
