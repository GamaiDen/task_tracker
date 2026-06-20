from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Task
from employees.models import Employee
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'executor']
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def important(self, request):
        """Важные задачи: не в работе, но от них зависят задачи в работе."""
        # Сначала найдём родителей, у которых статус 'in_progress'
        parents_in_progress = Task.objects.filter(status='in_progress')

        # Теперь найдём дочерние задачи к этим родителям, которые ещё новые
        important = Task.objects.filter(
            parent_task__in=parents_in_progress,
            status='new'
        ).distinct()

        result = []
        for task in important:
            least_busy = Employee.objects.annotate(
                active_count=Count('tasks', filter=Q(tasks__status='in_progress'))
            ).order_by('active_count').first()

            parent_executor = task.parent_task.executor if task.parent_task else None

            suggested = []
            if parent_executor:
                parent_active = parent_executor.tasks.filter(status='in_progress').count()
                if least_busy and parent_active <= (least_busy.tasks.filter(status='in_progress').count() + 2):
                    suggested.append(parent_executor.full_name)
                else:
                    suggested.append(least_busy.full_name if least_busy else 'Нет свободных')
            else:
                suggested.append(least_busy.full_name if least_busy else 'Нет свободных')

            result.append({
                'task': task.name,
                'deadline': task.deadline,
                'suggested_employees': suggested,
            })

        return Response(result)
