import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from backend.context import get_tenant_db


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, using=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        if user.is_superuser:
            using = 'default'
        user.save(using=using or self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

    def get_mirrored_superuser(self, superuser, db):
        user, created = User.objects.using(db).update_or_create(
            username=superuser.username,
            defaults=dict(
                is_staff=True,
                email=superuser.email,
                is_active=True,
                is_superuser=True,
            )
        )
        return user

    def get_superuser_for_app(self, **filters):
        db = get_tenant_db()
        auth_user = User.objects.using('default').filter(**filters, is_superuser=True).first()
        if auth_user:
            if db == 'default':
                superuser = auth_user
                return auth_user, superuser
            return auth_user, User.objects.get_mirrored_superuser(auth_user, db)
        return None, None


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    objects = UserManager()
