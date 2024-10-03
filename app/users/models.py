import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    supabase_id = models.CharField(
        unique=True,
        null=True,
        blank=True,
        default=None,
        max_length=255
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    profile_pic = models.URLField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'


class UserHabit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    habit = models.ForeignKey(
        'habits.Habit',
        on_delete=models.CASCADE
    )
    start_date = models.DateTimeField()
    current_streak = models.IntegerField(
        default=0
    )
    best_streak = models.IntegerField(
        default=0
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
    total_days_completed = models.IntegerField(
        default=0
    )
    next_milestone = models.IntegerField()
    next_skill_unlock = models.CharField(
        max_length=255
    )
    progress_percentage = models.FloatField(
        default=0.0
    )
    notifications_enabled = models.BooleanField(
        default=True
    )
    habit_logs = JSONField()
    completion_date = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.user.email} - {self.habit.name}'
