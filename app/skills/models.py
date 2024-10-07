from django.db import models
import uuid


class Skill(models.Model):
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
    description = models.TextField(
        blank=True,
        null=True
    )
    points = models.IntegerField(
        default=0
    )
    milestones = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.name
