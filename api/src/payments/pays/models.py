import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


class Payment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.PositiveIntegerField(default=0)
    organisation_id = models.UUIDField()
    attributes = JSONField()
