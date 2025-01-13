from django.db import models

from backend.context import get_tenant_subdomain

from users.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}@{get_tenant_subdomain()}'


class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}@{get_tenant_subdomain()}'


class Customer(User):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username}@{get_tenant_subdomain()}'

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
