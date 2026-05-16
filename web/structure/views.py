from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Department, Employee
from .serializers import DepartmentSerializer, DepartmentUpdateSerializer, EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']:
            return DepartmentUpdateSerializer
        return DepartmentSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter('depth', type=int, default=1, description='Глубина дерева (max 5)'),
            OpenApiParameter('include_employees', type=bool, default=True)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        department = self.get_object()
        
        try:
            depth = min(int(request.query_params.get('depth', 1)), 5)
        except ValueError:
            depth = 1
            
        include_employees = request.query_params.get('include_employees', 'true').lower() == 'true'

        def build_tree(dept, current_depth):
            data = DepartmentSerializer(dept).data
            if include_employees:
                data['employees'] = EmployeeSerializer(dept.employees.all(), many=True).data
            
            if current_depth < depth:
                data['children'] = [build_tree(child, current_depth + 1) for child in dept.children.all()]
            else:
                data['children'] = []
            return data

        return Response(build_tree(department, 1))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        if 'cycle_detected' in str(serializer.errors.get('parent_id', '')):
            return Response({"error": "Создание цикла невозможно"}, status=status.HTTP_409_CONFLICT)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter('mode', type=str, required=True, enum=['cascade', 'reassign']),
            OpenApiParameter('reassign_to_department_id', type=int, required=False)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        department = self.get_object()
        mode = request.query_params.get('mode')

        if mode == 'cascade':
            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        elif mode == 'reassign':
            reassign_to_id = request.query_params.get('reassign_to_department_id')
            if not reassign_to_id:
                return Response({"error": "Требуется reassign_to_department_id"}, status=status.HTTP_400_BAD_REQUEST)
                
            target_department = get_object_or_404(Department, pk=reassign_to_id)
            
            with transaction.atomic():
                department.employees.update(department=target_department)
                department.children.update(parent=target_department)
                department.delete()
                
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        return Response({"error": "Укажите mode (cascade или reassign)"}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        department_id = self.kwargs.get('department_id')
        department = get_object_or_404(Department, pk=department_id)
        serializer.save(department=department)