from backend.context import get_tenant_db


class DBRouter:

    def db_for_read(self, model, **hints):  # noqa
        return get_tenant_db()

    def db_for_write(self, model, **hints):  # noqa
        return get_tenant_db()

    def allow_migrate(self, db, app_label, model_name=None, **hints):  # noqa
        print(f'db {db} app_label {app_label} model_name {model_name}')
        if app_label == 'tenants':
            return db == 'default'
        elif app_label == 'app':
            return db != 'default' or model_name == 'user'
        return True
