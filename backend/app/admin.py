from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Organization, Department
from app.sites import application_site
from django.utils.translation import gettext_lazy as _


class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ("id", "email", "auth_token", 'is_active', 'is_staff', 'department')
    fieldsets = (
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "usable_password", "password1", "password2", "department"),
            },
        ),
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "department")


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name",)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")


application_site.register(Customer, CustomerAdmin)
application_site.register(Organization, OrganizationAdmin)
application_site.register(Department, DepartmentAdmin)
