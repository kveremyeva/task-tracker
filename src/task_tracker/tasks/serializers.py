from rest_framework import serializers
from .models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения задач"""
    assignee_name = serializers.CharField(source='assignee.full_name', read_only=True)
    parent_task_title = serializers.CharField(source='parent_task.title', read_only=True)

    class Meta:
        model = Tasks
        fields = '__all__'
