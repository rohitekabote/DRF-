
import re
from venv import create
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from blogs.serializers import BlogSerializer
import employees
from students.models import Student
from .serializers import studentserializer, employeeserializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommemtSerializer
from .pagination import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter, OrderingFilter

from api import serializers




# Create your views here.
@api_view(['GET', 'POST'])
def studentsview(request):
    # students = {
    #     'id':1,
    #     'name': 'Raju',
    #     'age': 34
    # }
    # students = Student.objects.all()
    # print(students)
    # student_list = list(students.values())
    # return JsonResponse(student_list, safe=False)
    if request.method == 'GET':
        # get all data from the Student table
        student = Student.objects.all()
        serializer = studentserializer(student, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = studentserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def studentdetailview(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer = studentserializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = studentserializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# class Employees(APIView):
    
#     def get(self, request):
#         employees = Employee.objects.all()
#         serializer = employeeserializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = employeeserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
# class EmployeeDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk):
#         employees = self.get_object(pk)
#         serializer = employeeserializer(employees)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = employeeserializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
  
#mixins      
'''class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = employeeserializer
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
class EmployeeDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = employeeserializer
    
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)'''
    
    
'''# generics
# class Employees(generics.ListAPIView, generics.CreateAPIView):
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = employeeserializer


# class EmployeeDetails(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = employeeserializer
    lookup_field = 'pk'
'''

'''class EmployeeViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = employeeserializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = employeeserializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = employeeserializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = employeeserializer(employee, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    
    def delete(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=None)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''
        
class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = employeeserializer
    pagination_class = CustomPagination
    # filterset_fields = ['designation']
    filterset_class = EmployeeFilter
    
class Blogviews(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['^blog_title', 'blog_body']
    ordering_fields = ['id', 'blog_title']
    
class Commentviews(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommemtSerializer
    
    
class blogdetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class commentdetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommemtSerializer
    lookup_field = 'pk'
    