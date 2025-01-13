import os
import glob


def get_tenant_files(tenant_folder):
    return glob.glob(os.path.join(tenant_folder, "*.py"))


def get_tenant_modules(tenant_folder):
    files = get_tenant_files(tenant_folder)
    return [os.path.basename(file_path)[:-3] for file_path in files]
