import logging
from contextlib import suppress

from django.apps import AppConfig


logger = logging.getLogger(__name__)


class TenantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenants'

    def ready(self):
        import tenants.signals  # noqa
