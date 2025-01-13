from adrf.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from .models import Organization, Department
from .serializers import OrganizationSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated


class OrganizationViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class DepartmentViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

