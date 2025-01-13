from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from app.models import Customer
from tenants.models import AdminUser
from users.models import User


@receiver(post_save, sender=User)
@receiver(post_save, sender=AdminUser)
@receiver(post_save, sender=Customer)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.using(instance._state.db).create(user=instance)
