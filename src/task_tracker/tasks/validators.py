from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_deadline_not_past(value):
    """Проверка, что срок выполнения не в прошлом."""
    if value < timezone.now().date():
        raise ValidationError("Срок выполнения не может быть в прошлом.")
    return value


def validate_active_task_has_assignee(status, assignee):
    """Проверка, что задача в работе имеет исполнителя."""
    if status == 'active' and not assignee:
        raise ValidationError("Для задачи в работе должен быть назначен исполнитель.")
    return True
