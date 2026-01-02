from django.db import models

class Employee(models.Model):
    """ Модель сотрудников"""
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Отчество')
    position = models.CharField(max_length=200, verbose_name='Должность')

    @property
    def full_name(self):
        """Возвращает полное ФИО (например, 'Иванов Иван Иванович')"""
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return " ".join(parts)


    def __str__(self):
        return f"{self.full_name} - {self.position}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']
