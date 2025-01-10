from asyncio import sleep
from contextlib import suppress

import faker
import pytest
from rest_framework import status
from app.models import Organization, Department
from django.urls import reverse
import pytest_asyncio
from adrf.test import AsyncAPIClient


@pytest.fixture
def api_client():
    return AsyncAPIClient()


async def try_delete(obj):
    with suppress(Exception):
        await obj.adelete()


@pytest_asyncio.fixture
async def organization():
    org = await Organization.objects.acreate(name="Test Organization")
    yield org
    await try_delete(org)


@pytest_asyncio.fixture
async def department(organization):
    dept = await Department.objects.acreate(organization=organization, name="Test Department")
    yield dept
    await try_delete(dept)


@pytest.mark.django_db
@pytest.mark.asyncio
class TestOrganizationViewSet:

    async def test_create_organization(self, api_client):
        response = await api_client.post(reverse('organization-list'), {'name': 'New Organization'})
        assert response.status_code == status.HTTP_201_CREATED
        assert await Organization.objects.acount() == 1
        assert (await Organization.objects.afirst()).name == 'New Organization'

    async def test_get_organization(self, organization, api_client):
        response = await api_client.get(reverse('organization-detail', args=[organization.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == organization.name

    async def test_update_organization(self, organization, api_client):
        response = await api_client.patch(reverse('organization-detail', args=[organization.id]), {'name': 'Updated Organization'})
        assert response.status_code == status.HTTP_200_OK
        await organization.arefresh_from_db()
        assert organization.name == 'Updated Organization'

    async def test_delete_organization(self, organization, api_client):
        response = await api_client.delete(reverse('organization-detail', args=[organization.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await Organization.objects.acount()) == 1


@pytest.mark.django_db
@pytest.mark.asyncio
class TestDepartmentViewSet:

    async def test_create_department(self, api_client, organization):
        response = await api_client.post(reverse('department-list'), {'name': 'New Department', 'organization': organization.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert await Department.objects.acount() == 1
        assert (await Department.objects.afirst()).name == 'New Department'

    async def test_get_department(self, department, api_client):
        response = await api_client.get(reverse('department-detail', args=[department.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == department.name

    async def test_update_department(self, department, api_client):
        response = await api_client.patch(reverse('department-detail', args=[department.id]), {'name': 'Updated Department'})
        assert response.status_code == status.HTTP_200_OK
        await department.arefresh_from_db()
        assert department.name == 'Updated Department'

    async def test_delete_department(self, department, api_client):
        response = await api_client.delete(reverse('department-detail', args=[department.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await Department.objects.acount()) == 0


# test_dbs = [
#     'a403b5a6-bdb6-4e1c-ade2-8ddf729fe995', "ca34168a-93ba-4c82-a318-ce9345ee2c6f",
# ]
#
#
# @pytest.mark.django_db(databases=test_dbs)
# @pytest.mark.asyncio
# class TestSimultaneousAccessDifferentDB:
#     async def test_simultaneous_access_different_db(self, api_client):
#         f = faker.Faker()
#
#         for i in range(20):
#             responses = []
#             for j in range(len(test_dbs)):
#                 responses.append(
#                     api_client.get(reverse('throttle_db_operations'), headers={'X-Tenant-ID': test_dbs[j]})
#                 )
#                 await sleep(0.01 * f.random_int(1, 5, 1))
#             assert [(await r).json()['tenant-id'] for r in responses] == test_dbs
