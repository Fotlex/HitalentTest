from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeCreateAPIView

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
    path('departments/<int:department_id>/employees/', EmployeeCreateAPIView.as_view(), name='employee-create'),
]