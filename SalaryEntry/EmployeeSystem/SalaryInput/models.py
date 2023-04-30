from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Employee(models.Model):
    SID = models.IntegerField(primary_key=True)
    chi_name = models.CharField(max_length=8, blank = True)
    eng_name = models.CharField(max_length=30, blank = True)
    class Meta:
        ordering = ['SID', 'chi_name']

class Salary(models.Model):
    pid = models.CharField(max_length=7, primary_key=True, default="", editable=False)
    month = models.CharField(max_length=4)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=3000, blank = True)
    pay_status = models.CharField(max_length=10)
    class Meta:
        ordering = ['month']
    def save(self, *args, **kwargs):
        self.pid = str(self.employee.SID) + '_' + str(self.month)
        super(Salary, self).save(*args, **kwargs)

    
