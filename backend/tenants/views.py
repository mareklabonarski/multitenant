import logging

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def hello(request):
    logging.info(request.headers)
    return JsonResponse({'tenant-id': request.headers.get('X-Tenant-ID', 'default')})
