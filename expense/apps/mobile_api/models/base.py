from django.db import models
from django.conf import settings
from django.utils.functional import cached_property


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseUserModel(BaseTimeStampModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s"
    )

    class Meta:
        abstract = True

class BaseModel(BaseTimeStampModel):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True
