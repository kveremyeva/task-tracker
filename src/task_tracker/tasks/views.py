from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tasks
from .serializers import TasksSerializer
from .filters import TasksFilter
from ..employees.models import Employee
from ..employees.serializers import EmployeeSerializer


class TasksViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Tasks - управление задачами сотрудников"""

    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = TasksFilter
    ordering_fields = ('id', 'status', 'deadline', 'created_at')

    def list(self, request, *args, **kwargs):
        """Вывод списка задач с поддержкой фильтра important_tasks"""
        filter_params = request.query_params

        if filter_params.get("important_tasks") == "true":
            # Запрос для поиска важных задач
            queryset = Tasks.objects.filter(status='inactive', id__in=Tasks.objects.filter(
                    parent_task__isnull=False,status='active'
            ).values_list('parent_task_id', flat=True).distinct()).distinct()
            serializer = self.get_serializer(queryset, many=True)
            formatted_response = []

            # Получаем всех сотрудников для анализа загрузки
            employees_data = EmployeeSerializer(Employee.objects.all(), many=True).data
            employee_active_tasks = {}
            for employee in Employee.objects.all():
                active_tasks_count = Tasks.objects.filter(
                    assignee=employee,
                    status='active'
                ).count()
                employee_active_tasks[employee.id] = active_tasks_count

            # Находим минимальную загрузку среди всех сотрудников
            min_count_tasks = min(employee_active_tasks.values()) if employee_active_tasks else 0

            least_busy_employees = []

            for employee_data in employees_data:
                emp_id = employee_data['id']
                if employee_active_tasks.get(emp_id, 0) == min_count_tasks:
                    least_busy_employees.append(employee_data)

            for item in serializer.data:
                task_obj = Tasks.objects.get(id=item['id'])
                parent_task = task_obj.parent_task

                # Проверяем есть ли у задачи родитель и назначен ли ему исполнитель
                if parent_task and parent_task.assignee:
                    related_employee = parent_task.assignee
                    count_task_related_employee = Tasks.objects.filter(
                        assignee=related_employee,
                        status='active'
                    ).count()

                    # Проверяем условие: если загружен не более чем на 2 задачи больше минимальной
                    if count_task_related_employee <= min_count_tasks + 2:
                        employee_names = [related_employee.full_name]
                    else:
                        employee_names = [emp['full_name'] for emp in least_busy_employees]
                else:
                    # Если нет родителя или у родителя нет исполнителя
                    employee_names = [emp['full_name'] for emp in least_busy_employees]

                # Формируем ответ в требуемом формате
                formatted_response.append({
                    "Важная задача": item['title'],
                    "Срок": item['deadline'],
                    "Исполнители": employee_names,
                })

            return Response(formatted_response)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BusyEmployeesView(APIView):
    """View для получения списка занятых сотрудников"""

    def get(self, request):
        """
        Возвращает список сотрудников, отсортированный по количеству активных задач
        Формат: от самого загруженного к наименее загруженному
        """
        # Получаем всех сотрудников
        employees = Employee.objects.all()

        result = []

        # Для каждого сотрудника считаем активные задачи
        for employee in employees:
            active_tasks_count = Tasks.objects.filter(
                assignee=employee,
                status='active'
            ).count()

            # Получаем сами активные задачи (опционально, для детализации)
            active_tasks = Tasks.objects.filter(
                assignee=employee,
                status='active'
            ).values('id', 'title', 'deadline')[:5]

            # Формируем данные сотрудника
            employee_data = {
                'employee_id': employee.id,
                'full_name': employee.full_name,
                'position': employee.position,
                'active_tasks_count': active_tasks_count,
                'active_tasks': list(active_tasks)
            }

            result.append(employee_data)

        # СОРТИРОВКА: по количеству активных задач (от большего к меньшему)
        result.sort(key=lambda x: x['active_tasks_count'], reverse=True)

        return Response(result)
