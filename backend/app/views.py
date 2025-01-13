import logging
from asyncio import sleep

import faker
from django.http import JsonResponse

from app.models import Organization


def hello(request):
    logging.info(request.headers)
    return JsonResponse({'tenant-id': request.headers.get('X-Tenant-ID', 'default')})


async def throttle_db_operations(request):
    f = faker.Faker()

    for i in range(6):
        created = await Organization.objects.acreate(name=f.country())
        await sleep(0.01 * f.random_int(1, 5, 1))
        organization = await Organization.objects.aget(id=created.id)
        assert created.name == organization.name
        await sleep(0.01 * f.random_int(1, 5, 1))

    return JsonResponse({'tenant-id': request.headers.get('X-Tenant-ID', 'default')})
