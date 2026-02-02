from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для CRUD операций с сотрудниками"""
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
