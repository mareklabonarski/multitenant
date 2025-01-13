import uuid
from django.db import models

from users.models import User



class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    subdomain = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)


class AdminUser(User):

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def save(self, *args, **kwargs):
        self.is_superuser = True
        # TODO ensure unique username across all db's  - this user will be mirrored
        return super().save(*args, **kwargs)
