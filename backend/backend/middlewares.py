import logging
from contextlib import contextmanager, asynccontextmanager
from django.http import Http404
from asgiref.sync import iscoroutinefunction

from backend.context import tenant_context, get_tenant_db

from tenants.models import Tenant

logger = logging.getLogger(__name__)


@contextmanager
def with_tenant_context(request):
    db = request.headers.get('X-Tenant-ID', 'default')
    subdomain = request.headers.get('X-Tenant-Subdomain', '')

    if subdomain and not Tenant.objects.using("default").filter(subdomain=subdomain, is_active=True).exists():
        raise Http404('Tenant {} not found'.format(subdomain))
    else:
        token = tenant_context.set({
            'db': db,
            'subdomain': subdomain
        })

    yield
    if token:
        tenant_context.reset(token)


@asynccontextmanager
async def awith_tenant_context(request):
    db = request.headers.get('X-Tenant-ID', 'default')
    subdomain = request.headers.get('X-Tenant-Subdomain', '')

    if subdomain and not await Tenant.objects.using("default").filter(subdomain=subdomain, is_active=True).aexists():
        raise Http404('Tenant {} not found'.format(subdomain))
    else:
        token = tenant_context.set({
            'db': db,
            'subdomain': subdomain
        })

    yield
    if token:
        tenant_context.reset(token)


def use_tenant_db_middleware(get_response):
    if iscoroutinefunction(get_response):
        async def middleware(request):
            async with awith_tenant_context(request):
                return await get_response(request)
    else:
        def middleware(request):
            with with_tenant_context(request):
                return get_response(request)

    return middleware


def allowed_path(request):
    is_default_db = get_tenant_db() == 'default'
    is_tenant_app = request.path.startswith('/tenants')
    return (is_default_db and is_tenant_app) or (not is_default_db and not is_tenant_app)


def path_restrictions_middleware(get_response):
    if iscoroutinefunction(get_response):
        async def middleware(request):
            if not allowed_path(request):
                raise Http404
            return await get_response(request)
    else:
        def middleware(request):
            if not allowed_path(request):
                raise Http404
            return get_response(request)

    return middleware

