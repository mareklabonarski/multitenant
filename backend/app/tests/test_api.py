from asyncio import sleep

import pytest
import faker
from rest_framework import status
from app.models import Organization, Department
from django.urls import reverse


@pytest.mark.django_db(databases=['default', 'TENANT_1'])
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, payload",
    [
        (reverse('organization-list'), {'name': 'New Organization'}),
        (reverse('organization-detail', args=[1]), {}),

        (reverse('department-list'), {'name': 'New Department', 'organization': 1}),
        (reverse('department-detail', args=[1]), {}),
    ],
)
async def test_unauthorized_access(api_client, endpoint, payload, tenant_1_headers):
    if callable(endpoint):
        endpoint = endpoint()

    response = await api_client.post(endpoint, payload, headers=tenant_1_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await api_client.get(endpoint, headers=tenant_1_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await api_client.patch(endpoint, payload, headers=tenant_1_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await api_client.delete(endpoint, headers=tenant_1_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db(databases=['default', 'TENANT_1'])
@pytest.mark.asyncio
class TestOrganizationViewSet:

    async def test_create(self, api_client, tenant_1_auth_headers):
        response = await api_client.post(
            reverse('organization-list'),
            {'name': 'New Organization'},
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Organization'

    async def test_get(self, organization, api_client, tenant_1_auth_headers):
        response = await api_client.get(
            reverse('organization-detail',
                    args=[organization.id]),
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == organization.name

    async def test_update(self, organization, api_client, tenant_1_auth_headers):
        response = await api_client.patch(
            reverse('organization-detail', args=[organization.id]),
            {'name': 'Updated Organization'},
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        await organization.arefresh_from_db(using='TENANT_1')
        assert organization.name == 'Updated Organization'

    async def test_delete(self, organization, api_client, tenant_1_auth_headers):
        response = await api_client.delete(
            reverse('organization-detail', args=[organization.id]),
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await Organization.objects.using('TENANT_1').filter(id=organization.id).acount()) == 0


@pytest.mark.django_db(databases=['default', 'TENANT_1'])
@pytest.mark.asyncio
class TestDepartmentViewSet:

    async def test_create(self, api_client, organization, tenant_1_auth_headers):
        response = await api_client.post(
            reverse('department-list'),
            {'name': 'New Department', 'organization': organization.id},
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Department'

    async def test_get(self, department, api_client, tenant_1_auth_headers):
        response = await api_client.get(
            reverse('department-detail', args=[department.id]),
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == department.name

    async def test_update(self, department, api_client, tenant_1_auth_headers):
        response = await api_client.patch(
            reverse('department-detail', args=[department.id]),
            {'name': 'Updated Department'},
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        await department.arefresh_from_db(using='TENANT_1')
        assert department.name == 'Updated Department'

    async def test_delete(self, department, api_client, tenant_1_auth_headers):
        response = await api_client.delete(
            reverse('department-detail', args=[department.id]),
            headers=tenant_1_auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await Department.objects.using('TENANT_1').filter(id=department.id).acount()) == 0


@pytest.mark.django_db(databases=['default', 'TENANT_1', 'TENANT_2'])
@pytest.mark.asyncio
class TestSimultaneousAccessDifferentDB:
    async def test_simultaneous_access_different_db(self, api_client):
        f = faker.Faker()

        for i in range(20):
            responses = []
            for tenant in ['TENANT_1', 'TENANT_2']:
                responses.append(
                    api_client.get(reverse('throttle_db_operations'), headers={'X-Tenant-ID': tenant})
                )
                await sleep(0.01 * f.random_int(1, 5, 1))
            assert [(await r).json()['tenant-id'] for r in responses] == ['TENANT_1', 'TENANT_2']


@pytest.mark.django_db(databases=['default', 'TENANT_1'])
@pytest.mark.asyncio
async def test_allowed_paths(api_client, tenant_1_headers, tenant_1_auth_headers):
    response = await api_client.get('/tenants', headers={'X-Tenant-ID': 'default'})
    assert response.status_code == 301
    response = await api_client.get('/tenants', headers=tenant_1_headers)
    assert response.status_code == 404
    response = await api_client.get('/tenants', headers=tenant_1_auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db(databases=['default', 'TENANT_1', 'TENANT_2'])
@pytest.mark.asyncio
async def test_db_router(api_client, tenant_1_auth_headers, tenant_2_auth_headers):
    common_id = 10000
    await Organization.objects.using('TENANT_1').acreate(id=common_id, name='TENANT_1')
    await Organization.objects.using('TENANT_2').acreate(id=common_id, name='TENANT_2')

    response = await api_client.get(
        reverse('organization-detail', args=[common_id]),
        headers=tenant_1_auth_headers
    )
    assert response.data['name'] == 'TENANT_1'

    response = await api_client.get(
        reverse('organization-detail', args=[common_id]),
        headers=tenant_2_auth_headers
    )
    assert response.data['name'] == 'TENANT_2'

    response = await api_client.get(
        reverse('organization-detail', args=[common_id]),
        headers={'X-Tenant-ID': 'default'}
    )
    assert response.status_code == 404
