from django.db import models

from ..employees.models import Employee


class Tasks(models.Model):
    """ Модель задач"""
    STATUS_CHOICE = [
        ('inactive', 'Не активна'),
        ('active', 'В работе'),
        ('complete', 'Выполнена')
    ]
    title = models.CharField(max_length=100, verbose_name="Наименование")
    parent_task = models.ForeignKey("self", on_delete=models.SET_NULL, null=True,
                                    blank=True, verbose_name="Родительская задача",
                                    related_name='subtasks')
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL,
                                 null=True, verbose_name="Исполнитель")
    deadline = models.DateTimeField(verbose_name='Срок')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE,
                              default='inactive', blank=True, null=True,
                              verbose_name="Статус выполнения")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
