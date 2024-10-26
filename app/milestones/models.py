from django.db import models
import uuid


class Milestone(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    name = models.CharField(
        max_length=255
    )
    day = models.IntegerField(
        default=0
    )
    points = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.name
