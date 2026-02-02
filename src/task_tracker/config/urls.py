from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Task Tracker API",
        default_version='v1',
        description="API для трекера задач сотрудников",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # API endpoints
    path('', include('task_tracker.employees.urls')),
    path('', include('task_tracker.tasks.urls')),

    # Документация API (Swagger/ReDoc)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
