from backend.context import get_tenant_db


class DBRouter:

    def db_for_read(self, model, **hints):  # noqa
        return get_tenant_db()

    def db_for_write(self, model, **hints):  # noqa
        return get_tenant_db()

    def allow_relation(self, *args, **kwargs):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):  # noqa
        if app_label == 'tenants':
            return db == 'default'
        elif app_label == 'app':
            return db != 'default'
        return True
