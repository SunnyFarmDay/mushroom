from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Employee(models.Model):
    SID = models.IntegerField()
    chi_name = models.CharField(max_length=8, blank = True)
    eng_name = models.CharField(max_length=30, blank = True)


class Salary(models.Model):
    month = models.CharField(max_length=2)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=3000, blank = True)
    pay_status = models.CharField(max_length=10)
    id = models.CharField(max_length=7, primary_key=True, default="", editable=False)

    def save(self, *args, **kwargs):
        self.id = str(self.employee.SID) + '_' + str(self.month)
        super(Salary, self).save(*args, **kwargs)

    
