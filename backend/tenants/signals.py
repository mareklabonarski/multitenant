# tenants/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    if sender.name == 'tenants':
        if not User.objects.filter(username='admin', is_superuser=True).exists():
            User.objects.create_superuser('admin@admin.pl', 'admin', 'admin')
            logger.info('Superuser admin created')
        else:
            logger.info('Superuser admin already exists')
