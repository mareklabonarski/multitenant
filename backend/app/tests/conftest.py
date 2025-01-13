from contextlib import suppress

import pytest
import pytest_asyncio
from adrf.test import AsyncAPIClient
from django.core.management import call_command
from django.db import connection
from rest_framework.authtoken.models import Token

from app.models import Organization, Department, Customer
from backend.test_settings import TENANT_1_ID, TENANT_2_ID
from tenants.models import Tenant


async def try_delete(obj):
    with suppress(Exception):
        await obj.adelete(using=obj._state.db)


@pytest.fixture(scope='session', autouse=True)
def tenant_1_db(django_db_blocker):
    with django_db_blocker.unblock():
        with connection._nodb_cursor() as cursor:
            cursor.execute(f'CREATE DATABASE "{TENANT_1_ID}"')
        call_command('migrate', database='TENANT_1')


@pytest.fixture(scope='session', autouse=True)
def tenant_2_db(django_db_blocker):
    with django_db_blocker.unblock():
        with connection._nodb_cursor() as cursor:
            cursor.execute(f'CREATE DATABASE "{TENANT_2_ID}"')
        call_command('migrate', database='TENANT_2')


@pytest_asyncio.fixture(autouse=True)
async def tenant_1():
    t = await Tenant.objects.acreate(id=TENANT_1_ID, name="TENANT_1", subdomain='tenant_1')
    yield t
    await try_delete(t)


@pytest_asyncio.fixture(autouse=True)
async def tenant_2():
    t = await Tenant.objects.acreate(id=TENANT_2_ID, name="TENANT_2", subdomain='tenant_2')
    yield t
    await try_delete(t)


@pytest.fixture
def api_client():
    return AsyncAPIClient()


@pytest_asyncio.fixture
async def organization():
    org = await Organization.objects.using('TENANT_1').acreate(name="Test Organization")
    yield org
    await try_delete(org)


@pytest_asyncio.fixture
async def department(organization):
    dept = await Department.objects.using('TENANT_1').acreate(organization=organization, name="Test Department")
    yield dept
    await try_delete(dept)


@pytest_asyncio.fixture
async def customer(department):
    customer = await Customer.objects.using('TENANT_1').acreate(department=department, username='customer')
    yield customer
    await try_delete(customer)


@pytest_asyncio.fixture
async def token(customer):
    return await Token.objects.using('TENANT_1').aget(user=customer)


@pytest.fixture
def auth_headers(token):
    return {'Authorization': f'Token {token}'}


@pytest.fixture
def tenant_1_headers(token):
    return {'X-Tenant-ID': 'TENANT_1'}


@pytest.fixture
def tenant_1_auth_headers(token):
    return {'X-Tenant-ID': 'TENANT_1', 'Authorization': f'Token {token}'}


@pytest_asyncio.fixture
async def organization_tenant_2():
    org = await Organization.objects.using('TENANT_2').acreate(name="Test Organization Tenant 2")
    yield org
    await try_delete(org)


@pytest_asyncio.fixture
async def department_tenant_2(organization_tenant_2):
    dept = await Department.objects.using('TENANT_2').acreate(organization=organization_tenant_2, name="Test Department Tenant 2")
    yield dept
    await try_delete(dept)


@pytest_asyncio.fixture
async def customer_tenant_2(department_tenant_2):
    customer = await Customer.objects.using('TENANT_2').acreate(department=department_tenant_2, username='customer_tenant_2')
    yield customer
    await try_delete(customer)


@pytest_asyncio.fixture
async def token_tenant_2(customer_tenant_2):
    return await Token.objects.using('TENANT_2').aget(user=customer_tenant_2)


@pytest.fixture
def auth_headers_tenant_2(token_tenant_2):
    return {'Authorization': f'Token {token_tenant_2}'}


@pytest.fixture
def tenant_2_headers(token_tenant_2):
    return {'X-Tenant-ID': 'TENANT_2'}


@pytest.fixture
def tenant_2_auth_headers(token_tenant_2):
    return {'X-Tenant-ID': 'TENANT_2', 'Authorization': f'Token {token_tenant_2}'}
