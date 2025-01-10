import contextvars

ContextVar = contextvars.ContextVar
tenant_context = ContextVar('tenant')
context_default = {
    'db': 'default',
    'subdomain': ''
}


def get_tenant_db():
    return tenant_context.get(context_default)['db']


def get_tenant_subdomain():
    return tenant_context.get(context_default)['subdomain']
