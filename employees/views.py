from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['position']
    search_fields = ['full_name']

    @action(detail=False, methods=['get'])
    def busy(self, request):
        """Сотрудники, отсортированные по количеству активных задач."""
        employees = Employee.objects.annotate(
            active_tasks=Count('tasks', filter=Q(tasks__status='in_progress'))
        ).order_by('-active_tasks')
        data = [{'full_name': e.full_name, 'active_tasks': e.active_tasks} for e in employees]
        return Response(data)
