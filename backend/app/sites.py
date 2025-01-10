from django.contrib import admin

from backend.context import get_tenant_db


class ApplicationAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return get_tenant_db() != 'default' and request.user.is_staff


application_site = ApplicationAdminSite(name='application-site')
