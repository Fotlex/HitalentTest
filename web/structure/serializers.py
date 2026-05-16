from rest_framework import serializers
from .models import Department, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'department_id', 'full_name', 'position', 'hired_at', 'created_at']
        read_only_fields = ['id', 'created_at', 'department_id']


class DepartmentSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=Department.objects.all(),
        allow_null=True,
        required=False,
        default=None
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent_id', 'created_at']

    def validate(self, data):
        name = data.get('name', self.instance.name if self.instance else None)
        
        if 'parent' in data:
            parent = data['parent']
        else:
            parent = self.instance.parent if self.instance else None
            
        qs = Department.objects.filter(name=name, parent=parent)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
            
        if qs.exists():
            raise serializers.ValidationError({"name": "Подразделение с таким именем уже существует в данном узле."})
            
        return data


class DepartmentUpdateSerializer(DepartmentSerializer):
    def validate(self, data):
        data = super().validate(data)
        
        if 'parent' not in data:
            return data
            
        new_parent = data['parent']
        
        if not new_parent:
            return data
            
        if new_parent.id == self.instance.id:
            raise serializers.ValidationError({"parent_id": "Подразделение не может быть родителем самого себя."})

        current = new_parent
        while current is not None:
            if current.id == self.instance.id:
                raise serializers.ValidationError({"parent_id": "cycle_detected"})
            current = current.parent
            
        return data