from django.contrib import admin

from backend.context import get_tenant_db


class TenantsSite(admin.AdminSite):
    def has_permission(self, request):
        return get_tenant_db() == 'default' and request.user.is_superuser


tenants_site = TenantsSite(name='tenants-site')
