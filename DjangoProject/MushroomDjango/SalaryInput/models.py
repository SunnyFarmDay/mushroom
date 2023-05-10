from django.db import models

# Create your models here.
class Class(models.Model):
    #Vi06045 II (intrument) GG (level) MMM (minutes per class)
    CID = models.CharField(max_length=20, primary_key=True, editable = False, default="")
    type = models.CharField(max_length=20)
    level = models.CharField(max_length=10)
    duration = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def save(self, *args, **kwargs):
        self.CID = self.type[:2] + self.level[:2] + str(self.duration)
        super(Class, self).save(*args, **kwargs)
    class Meta:
        ordering = ['type', 'duration', 'level']

class Employee(models.Model):
    SID = models.IntegerField(primary_key=True)
    chi_name = models.CharField(max_length=8, blank = True)
    eng_name = models.CharField(max_length=30, blank = True)
    classes = models.ManyToManyField(Class, default=None, blank=True)
    class Meta:
        ordering = ['SID', 'chi_name']

    def __str__(self):
        if self.chi_name:
            name = self.chi_name
        else:
            name = self.eng_name
        return name
class Salary(models.Model):
    PID = models.CharField(max_length=11, primary_key=True, default="", editable=False)
    month = models.CharField(max_length=4)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=3000, blank = True)
    pay_status = models.CharField(max_length=10)
    cheque_number = models.CharField(max_length=10, blank = True)
    created_time = models.DateField(auto_now_add=True)
    paid_time = models.DateField(blank = True, null=True)

    class Meta:
        ordering = ['month']
    def save(self, *args, **kwargs):
        id = 0
        PID = str(self.employee.SID) + '_' + str(self.month) + str(id)
        while Salary.objects.filter(PID = PID).first():
            id = id + 1
            PID = str(self.employee.SID) + '_' + str(self.month) + str(id)
        self.PID = PID
        super(Salary, self).save(*args, **kwargs)

    


# class Lesson(models.Model):
#     Class = models.ForeignKey(Class, on_delete=models.CASCADE)
#     usual_weekday = models.CharField(max_length=3)
#     usual_starttime = models.CharField(max_length=4)
#     usual_endtime = models.CharField(max_length=4)
#     actual_weekay = models.CharField(max_length=3)
#     actual_starttime = models.CharField(max_length=4)
#     actual_endtime = models.CharField(max_length=4)
#     attended = models.BooleanField(default=False)
#     paid = models.BooleanField(default=False)


