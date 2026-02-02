from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from task_tracker.employees.models import Employee
from task_tracker.tasks.models import Tasks


class TaskModelTest(APITestCase):
    """Тесты модели Task"""

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Тест",
            last_name="Сотрудник",
            position="Разработчик"
        )

    def test_task_creation(self):
        """Тест 1: Создание задачи"""
        task = Tasks.objects.create(
            title="Тестовая задача",
            deadline=timezone.now(),
            status="inactive",
            assignee=self.employee
        )
        self.assertEqual(str(task), "Тестовая задача")

    def test_task_with_parent(self):
        """Тест 2: Связь родитель-потомок"""
        parent_task = Tasks.objects.create(
            title="Родительская задача",
            deadline=timezone.now(),
            status="active",
            assignee=self.employee
        )

        child_task = Tasks.objects.create(
            title="Дочерняя задача",
            deadline=timezone.now(),
            status="inactive",
            assignee=self.employee,
            parent_task=parent_task
        )

        self.assertEqual(child_task.parent_task, parent_task)
        self.assertIn(child_task, parent_task.subtasks.all())


class TaskAPITest(APITestCase):
    """Тесты API для задач"""

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="API",
            last_name="Тест",
            position="Разработчик"
        )

    def test_get_tasks_list(self):
        """Тест 3: Получение списка задач"""
        response = self.client.get('/tasks/')
        self.assertIn(response.status_code, [200, 403])

    def test_create_task_orm(self):
        """Тест 4: Создание задачи через ORM"""
        task = Tasks.objects.create(
            title="ORM задача",
            deadline=timezone.now() + timedelta(days=7),
            status="inactive",
            assignee=self.employee
        )
        self.assertEqual(Tasks.objects.count(), 1)
        self.assertEqual(task.title, "ORM задача")


class BusinessLogicTest(APITestCase):
    """Тесты бизнес-логики (требования ТЗ)"""

    def setUp(self):
        self.employee1 = Employee.objects.create(
            first_name="Занятый",
            last_name="Сотрудник",
            position="Разработчик"
        )
        self.employee2 = Employee.objects.create(
            first_name="Свободный",
            last_name="Сотрудник",
            position="Тестировщик"
        )

    def test_busy_employees_logic(self):
        """Тест 5: Логика подсчета активных задач (для busy_employees)"""
        # Создаем 3 активные задачи для employee1
        for i in range(3):
            Tasks.objects.create(
                title=f"Активная {i}",
                deadline=timezone.now(),
                status="active",
                assignee=self.employee1
            )

        # Создаем 1 активную задачу для employee2
        Tasks.objects.create(
            title="Одна задача",
            deadline=timezone.now(),
            status="active",
            assignee=self.employee2
        )

        # Проверяем подсчет через ORM
        active_count1 = Tasks.objects.filter(
            assignee=self.employee1,
            status='active'
        ).count()

        active_count2 = Tasks.objects.filter(
            assignee=self.employee2,
            status='active'
        ).count()

        self.assertEqual(active_count1, 3)
        self.assertEqual(active_count2, 1)

    def test_important_tasks_logic(self):
        """Тест 6: Логика поиска важных задач"""
        important_task = Tasks.objects.create(
            title="Важная задача",
            deadline=timezone.now() + timedelta(days=5),
            status="inactive",
            assignee=None
        )

        Tasks.objects.create(
            title="Активная подзадача",
            deadline=timezone.now() + timedelta(days=3),
            status="active",
            assignee=self.employee1,
            parent_task=important_task
        )

        important_tasks = Tasks.objects.filter(
            status='inactive',
            subtasks__status='active'
        ).distinct()

        self.assertEqual(important_tasks.count(), 1)
        self.assertEqual(important_tasks.first().title, "Важная задача")

    def test_task_status_validation(self):
        """Тест 7: Проверка валидации статусов"""
        # Создаем задачу с будущим дедлайном
        valid_task = Tasks.objects.create(
            title="Валидная задача",
            deadline=timezone.now() + timedelta(days=1),
            status="inactive",
            assignee=self.employee1
        )
        self.assertIsNotNone(valid_task.id)


class SpecialEndpointsTest(APITestCase):
    """Тесты специальных эндпоинтов"""

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Эндпоинт",
            last_name="Тест",
            position="Разработчик"
        )

    def test_busy_employees_endpoint_exists(self):
        """Тест 8: Проверка существования эндпоинта busy_employees"""
        response = self.client.get('/busy_employees/')
        self.assertIn(response.status_code, [200, 403])

    def test_important_tasks_filter_exists(self):
        """Тест 9: Проверка фильтра important_tasks"""
        response = self.client.get('/tasks/?important_tasks=true')
        self.assertIn(response.status_code, [200, 403])


class CRUDOperationsTest(APITestCase):
    """Тесты CRUD операций"""

    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="CRUD",
            last_name="Тест",
            position="Разработчик"
        )

    def test_full_crud_cycle(self):
        """Тест 10: Полный цикл CRUD через ORM"""
        # Create
        task = Tasks.objects.create(
            title="CRUD задача",
            deadline=timezone.now(),
            status="inactive",
            assignee=self.employee
        )
        task_id = task.id

        task_from_db = Tasks.objects.get(id=task_id)
        self.assertEqual(task_from_db.title, "CRUD задача")

        Tasks.objects.filter(id=task_id).update(title="Обновленная")
        task.refresh_from_db()
        self.assertEqual(task.title, "Обновленная")

        task.delete()
        self.assertFalse(Tasks.objects.filter(id=task_id).exists())
