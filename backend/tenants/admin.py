import os, subprocess
import signal

import psycopg2
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from tenants.models import Tenant, AdminUser
from django.conf import settings
from django.core.management import call_command
from django.template.loader import render_to_string
import logging
from django.db import connection
from django.contrib import messages
from tenants.sites import tenants_site


def create_db_file(request, tenant):
    context = {
        'tenant_subdomain': tenant.subdomain,
        'tenant_id': tenant.id,
        'db_name': tenant.id,
        'db_host': settings.DATABASES['default']['HOST'],
        'db_port': settings.DATABASES['default']['PORT'],
        'db_user': settings.DATABASES['default']['USER'],   # normally would be from the model
        'db_password': settings.DATABASES['default']['PASSWORD'],  # normally would be from the model
    }

    database = render_to_string('database.txt', context)
    file_path = os.path.join(settings.TENANT_DB_DIR, f'{tenant.name}.py')
    with open(file_path, 'w') as file:
        file.write(database)

    messages.success(request, f'Created Database definition for {tenant.subdomain}: {tenant.id}')
    return True


def create_server_file(request, tenant):
    context = {
        'tenant_subdomain': tenant.subdomain,
        'tenant_id': tenant.id,
    }

    server = render_to_string('nginx-server.txt', context)
    file_path = os.path.join(settings.NGINX_CONF_DIR, f'{tenant.subdomain}.conf')
    with open(file_path, 'w') as file:
        file.write(server)
    messages.success(request, f'Created subdomain configuration in NGINX for {tenant.subdomain}: {tenant.id}')
    return True


def remove_server_file(request, tenant):
    try:
        result = subprocess.run(["rm", os.path.join(settings.NGINX_CONF_DIR, f'{tenant.subdomain}.conf')], check=True, text=True,
                                capture_output=True)
        logging.info("Remove output: ", result.stdout)
        messages.success(request, f'{tenant.subdomain} subdomain configuration removed')
        return True
    except subprocess.CalledProcessError:
        logging.exception("Could not delete nginx file", exc_info=True)
        messages.error(request, f'Could not delete nginx file for {tenant.subdomain}!')


def create_db(request, tenant):
    with connection._nodb_cursor() as cursor:
        try:
            cursor.execute(f'CREATE DATABASE "{str(tenant.id)}"')
        except psycopg2.errors.DuplicateDatabase:
            messages.info(request, f'Database for {tenant.subdomain} already exists')
        else:
            messages.success(request, f'Database for {tenant.subdomain} created')
            return True


def migrate_db(request, tenant):
    try:
        # run migrations
        output = call_command('migrate', database=str(tenant.id))
        messages.success(request, f'Database for {tenant.subdomain} migrated')
        return True
    except Exception as e:
        logging.exception(f"Could not run migration {e}", exc_info=True)
        messages.error(request, f'Error migrating database for {tenant.subdomain}!')


@admin.action(description='Deploy tenant (tenant database, django settings, nginx configuration)')
def create_tenant_settings(modeladmin, request, queryset):
    for tenant in queryset.filter(is_active=False):
        for step in [
            create_db_file,
            create_db,
            create_server_file,
        ]:
            if not step(request, tenant):
                break
    else:
        os.kill(1, signal.SIGUSR2)


@admin.action(description='Migrate tenant database')
def migrate_tenant_db(modeladmin, request, queryset):
    for tenant in queryset.filter(is_active=False):
        if str(tenant.id) not in settings.DATABASES:
            messages.error(request, f'Settings for {tenant.subdomain} are not yet loaded!')
            continue

        for step in [
            migrate_db,
        ]:
            if not step(request, tenant):
                break
        else:
            tenant.is_active = True
            tenant.save()


@admin.action(description='Switch off tenant (remove from nginx)')
def switch_off_tenant(modeladmin, request, queryset):
    for tenant in queryset.filter(is_active=True):
        remove_server_file(request, tenant)
        tenant.is_active = False
        tenant.save()


class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', "settings_loaded", 'is_active', 'link')
    actions = [create_tenant_settings, switch_off_tenant, migrate_tenant_db]

    def settings_loaded(self, obj):
        return str(obj.id) in settings.DATABASES

    def link(self, obj):
        return format_html('<a href="{0}">{0}</a>', f"http://{obj.subdomain}.localhost/application")


class AdminUserAdmin(UserAdmin):
    list_display = ("id", "email", "auth_token", 'is_active', 'is_staff', 'is_superuser')
    fieldsets = [(None, {"fields": ["email"]})]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_filter = ("is_active",)
    model = AdminUser


tenants_site.register(Tenant, TenantAdmin)
tenants_site.register(AdminUser, AdminUserAdmin)
