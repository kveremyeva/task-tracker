from rest_framework import serializers
from .models import Tasks
from .validators import validate_deadline_not_past, validate_active_task_has_assignee


class TasksSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения задач"""
    assignee_name = serializers.CharField(source='assignee.full_name', read_only=True)
    parent_task_title = serializers.CharField(source='parent_task.title', read_only=True)

    class Meta:
        model = Tasks
        fields = '__all__'
        extra_kwargs = {
            'deadline': {
                'validators': [validate_deadline_not_past]
            }
        }

    def validate(self, attrs):
        """Основная валидация для задачи"""
        status = attrs.get('status', getattr(self.instance, 'status', None))
        assignee = attrs.get('assignee', getattr(self.instance, 'assignee', None))
        if status == 'active':
            validate_active_task_has_assignee(status, assignee)

        return attrs
