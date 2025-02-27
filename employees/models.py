from django.db import models

# Create your models here.

class Employee(models.Model):
    emp_id = models.CharField(max_length=10)
    emp_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.emp_name