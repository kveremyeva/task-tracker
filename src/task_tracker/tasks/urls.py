from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TasksViewSet, BusyEmployeesView

router = DefaultRouter()
router.register(r'tasks', TasksViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('busy_employees/', BusyEmployeesView.as_view(), name='busy-employees'),
]
