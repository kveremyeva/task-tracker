from rest_framework import status
from rest_framework.test import APITestCase
from task_tracker.employees.models import Employee


class EmployeeModelTest(APITestCase):
    def test_employee_creation(self):
        employee = Employee.objects.create(
            first_name="Иван",
            last_name="Иванов",
            position="Разработчик"
        )
        self.assertEqual(employee.full_name, "Иванов Иван")
        self.assertEqual(str(employee), "Иванов Иван - Разработчик")

    def test_get_employees_list(self):
        """Тест 3: Получение списка сотрудников"""
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_employee(self):
        """Тест 4: Обновление сотрудника"""
        employee = Employee.objects.create(
            first_name="Старое",
            last_name="Имя",
            position="Старая должность"
        )

        data = {"position": "Новая должность"}
        response = self.client.patch(f'/employees/{employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
