from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from employees.models import Employee
from .serializers import employeeserializer



class EmployeeAPITestCase(TestCase):
    def setUp(self):
        print("Setting up")
        Employee.objects.create(
            emp_id = 'e009',
            emp_name = 'rohit',
            designation = 'developer',
        )
        Employee.objects.create(
            emp_id ='e0010',
            emp_name = 'ramesh',
            designation = 'project manager',
        )
        self.list_urls = reverse('employees-list')
        self.detail_urls = lambda id: reverse('employees-detail', kwargs={"pk":id})


    # Test for GET /employees
    def test_get_employee_list(self):
        print("get list_Employee")
        response = self.client.get(self.list_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employees = Employee.objects.all()
        self.assertEqual(employees.count(),2)

    def test_get_employee_list_no_employees(self):
        print("get list_Employee no employees")
        e=Employee.objects.all()
        e.delete()
        print(e)
        response = self.client.get(self.list_urls)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(e.count(), 0)
    
        
    def test_post_employee(self):
        print("post employee")
        data = {
            'emp_id': 'e0011',
            'emp_name': 'ramesh',
            'designation': 'project manager',
        }
        response = self.client.post(self.list_urls, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee = Employee.objects.get(emp_id='e0011')
        self.assertEqual(employee.emp_name, data['emp_name'])
        self.assertEqual(employee.designation, data['designation'])
        employee = Employee.objects.all()
        self.assertEqual(employee.count(),3)

    def test_get_employee_detail(self):
        print("get detail_employee")
        employee = Employee.objects.get(emp_id='e009')  
        response = self.client.get(self.detail_urls(employee.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['emp_name'], employee.emp_name)

    def test_put_employee_detail(self):
        print("put employee")
        employee = Employee.objects.get(emp_id='e009')
        print(employee)
        data = {
            'emp_id': 'e009',
            'emp_name': 'rohit updated',
            'designation': 'developer updated',
        }
        print(data)
        response = self.client.put(self.detail_urls(employee.pk), data, content_type='application/json' )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.emp_name, response.data['emp_name'])
        self.assertEqual(employee.designation, response.data['designation'])

    def test_delete_employee_detail(self):
        print("delete employee")
        employee = Employee.objects.get(emp_id='e009')
        print(employee.designation)
        response = self.client.delete(self.detail_urls(employee.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(Employee.DoesNotExist, Employee.objects.get, emp_id='e009')


