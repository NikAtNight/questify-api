import uuid

from django.db import models


class Base(models.Model):
    """Base"""

    # Fields
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255,
        unique=True
    )

    # Magic
    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        abstract = True


class Category(Base):
    """Category"""

    class Meta:
        ordering = ['name']
