from django.db import models


class Employee(models.Model):
    employee_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()

    def __str__(self):
        return f"{self.employee_code} - {self.name}"
    
    
    

class LeaveBalance(models.Model):
    employee = models.OneToOneField(Employee,on_delete=models.CASCADE,related_name="leave_balance")
    year = models.PositiveIntegerField()
    total_leaves = models.PositiveIntegerField(default=0)
    used_leaves = models.PositiveIntegerField(default=0)
    remaining_leaves = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.employee.name} - {self.year}"