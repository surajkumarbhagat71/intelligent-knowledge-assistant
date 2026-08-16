from django.contrib import admin
from .models import Employee, LeaveBalance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_code",
        "name",
        "email",
        "department",
        "designation",
        "joining_date",
    )
    search_fields = (
        "employee_code",
        "name",
        "email",
    )
    list_filter = (
        "department",
        "designation",
    )
    
    
admin.site.register(LeaveBalance)