from django.urls import path, include
from tenants.sites import tenants_site


urlpatterns = [
    path('', tenants_site.urls),
]
