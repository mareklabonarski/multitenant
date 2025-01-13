import logging

from django.http import JsonResponse


def hello(request):
    logging.info(request.headers)
    return JsonResponse({'tenant-id': request.headers.get('X-Tenant-ID', 'default')})
