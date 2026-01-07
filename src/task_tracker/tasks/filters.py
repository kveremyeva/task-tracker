import django_filters
from django.db.models import Q

from .models import Tasks


class TasksFilter(django_filters.FilterSet):
    """Фильтры для модели Tasks"""

    # Фильтрует по статусу задачи
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    # Фильтрует по наличию родительской задачи
    parent_task_isnull = django_filters.BooleanFilter(field_name="parent_task", lookup_expr="isnull")

    # Фильтрует по статусу родительской задачи
    parent_task_status = django_filters.CharFilter(field_name="parent_task__status", lookup_expr="exact")

    # Фильтрует по исполнителю
    assignee = django_filters.NumberFilter(field_name="assignee__id", lookup_expr="exact")

    # Фильтрует по наличию исполнителя
    assignee_isnull = django_filters.BooleanFilter(field_name="assignee", lookup_expr="isnull")

    # Фильтрует задачи и выводит только важные
    # (которые не взяты в работу, но имеют подзадачи, которые взяты в работу)
    important_tasks = django_filters.BooleanFilter(method='filter_important_tasks')

    class Meta:
        model = Tasks
        fields = [
            'status',
            'parent_task_isnull',
            'parent_task_status',
            'assignee',
            'assignee_isnull',
            'important_tasks'
        ]

    def filter_important_tasks(self, queryset, name, value):
        """Метод для вывода только важных задач"""
        if value:
            status_check = queryset.filter(status="inactive")
            has_subtasks_check = queryset.filter(subtasks__isnull=False)
            subtasks_active_check = queryset.filter(subtasks__status="active")
            return queryset.filter(
                Q(pk__in=status_check) &
                Q(pk__in=has_subtasks_check) &
                Q(pk__in=subtasks_active_check)
            ).distinct()

        return queryset
