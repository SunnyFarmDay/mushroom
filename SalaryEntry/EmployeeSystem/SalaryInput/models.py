from django.db import models

# Create your models here.
class Employee(models.Model):
    SID = models.IntegerField()
    ChiName = models.CharField(max_length=8, blank = True)
    EngName = models.CharField(max_length=30, blank = True)

class Salary(models.Model):
    month = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
