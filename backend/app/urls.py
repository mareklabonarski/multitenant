from . import views
from rest_framework.authtoken import views as auth_views
from app.sites import application_site

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import OrganizationViewSet, DepartmentViewSet


router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'departments', DepartmentViewSet)


urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('api/', include(router.urls)),
    path('throttle/', views.throttle_db_operations, name='throttle_db_operations'),
    path('', application_site.urls),
]
