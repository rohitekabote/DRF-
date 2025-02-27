from rest_framework import serializers
from students.models import Student
from employees.models import Employee

class studentserializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields= "__all__"
        
class employeeserializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        DESIGNATION_CHOICES = ['Developer', 'Manager', 'HR', 'Engineer']
        fields = "__all__"

    def validate_emp_id(self, value):
        if not value.startswith('e'):
            raise serializers.ValidationError("Employee ID must start with 'e'.")
        if Employee.objects.filter(emp_id=value).exists():
            raise serializers.ValidationError("Employee ID already exists")
        return value
    
    def validate(self, value):
        if value['emp_name'] == value['designation']:
            raise serializers.ValidationError("Name and Designation cannot be the same.")
            
        return value
    
    def validate_emp_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Employee Name cannot contain digits.")
        return value

    def validate_designation(self, value):
        if value not in self.DESIGNATION_CHOICES:
            raise serializers.ValidationError("Invalid Designation.")
        return value
