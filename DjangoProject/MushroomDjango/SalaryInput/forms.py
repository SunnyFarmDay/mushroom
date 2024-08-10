from django import forms
from .models import Employee, Class, Salary
from datetime import datetime
from django.utils import timezone
from .const import *
import re
thismonth = str(int(datetime.now().strftime("%Y%m")[2:]) - 1)

def validateAndFormatChequeNumber(input):
    input = input.split('-')
    if len(input) != 2:
        raise ValueError("Cheque format is incorrect (e.g. BOC-123456)")
    if len(input[1]) !=6:
        raise ValueError("Cheque format is incorrect (e.g. BOC-123456)")
    return input

def validateChequeNumberAndPayStatus(cheque, status):
    if cheque:
        cheque = validateAndFormatChequeNumber(cheque)
    if status not in PAY_STATUS_LIST:
        raise ValueError(f'Pay Status can only be {PAY_STATUS_LIST}!')
    if status == 'P':
        if not cheque:
            raise SyntaxError("Pay status is P while having no cheque number!")
    else:
        if cheque:
            raise ValueError("Please update Pay Status to P if you already have cheque number!")
    return cheque

class EmployeeSalarySelectionForm(forms.Form):

    month = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'YYMM', 'class': "form-control text-end"}))
    SID_or_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'SID or Name', 'class': "form-control text-end", 'list': 'Employee_names_list','aria-label':"SID_or_name", 'aria-describedby':"SID_or_name"}))
    employee = forms.ModelChoiceField(Employee.objects.all(), required=False)
    new_employee = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned = super().clean()
        errors = []
        SID_or_name = cleaned.get("SID_or_name")
        if (not SID_or_name):
            raise forms.ValidationError("SID_or_name cannot be blank")
        if str(SID_or_name).isnumeric():
            SID = int(SID_or_name)
            if len(str(SID_or_name)) != 4:
                errors.append(forms.ValidationError("SID should be 4 digits"))
            else:
                try:
                    employee = Employee.objects.get(SID=SID)
                    cleaned['employee']=employee
                except Employee.DoesNotExist:
                    errors.append(forms.ValidationError("SID does not match"))
                except:
                    errors.append(forms.ValidationError("Unknown Error01"))
        else:
            name = str(SID_or_name)
            if len(SID_or_name) < 4:
                chi_name = name
                eng_name = ''
            else:
                chi_name = ''
                eng_name = name
            try:
                if chi_name:
                    employee = Employee.objects.get(chi_name = name)
                else:
                    employee = Employee.objects.get(eng_name = name)
                cleaned['employee'] = employee
            except Employee.DoesNotExist:
                SID = Employee.objects.values("SID").order_by("SID").last()
                if SID:
                    SID = SID['SID']
                    SID = SID + 1
                    employee = Employee.objects.create(SID=SID, chi_name = chi_name, eng_name = eng_name)
                    cleaned['new_employee']=True
                    cleaned['employee'] = employee
                else: 
                    errors.append(forms.ValidationError("Unknown Error 02"))
            except:
                errors.append(forms.ValidationError("Unknown Error 03"))
        if len(str(cleaned['month'])) != 4:
            errors.append(forms.ValidationError("Month should be in format of YYMM"))
        month = int(str(cleaned['month'])[2:])
        if month < 0 or month > 12:
            errors.append(forms.ValidationError("Month should within 0 to 12"))
        if errors:
            raise forms.ValidationError(errors)
        
        return cleaned



# class SalaryRecordForm(forms.Form):
#     pay_status_choices = (
#         ('N', 'N'),
#         ('M', 'M'),
#         ('P', 'P'),
#     )
#     SID_or_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'SID or Name', 'class': "form-control SID_field", 'list': 'Employee_names_list','aria-label':"SID_or_name", 'aria-describedby':"SID_or_name"}))
#     amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': "form-control amount_field"}))
#     description = forms.CharField(max_length=3000, required=False,widget=forms.Textarea(attrs={'class': "form-control textarea description_field", 'placeholder': "*description"}))
#     pay_status = forms.ChoiceField(choices = pay_status_choices, widget=forms.Select(attrs={'class': "form-control pay_status_field"}))
#     employee = forms.ModelChoiceField(Employee.objects.all(), required=False)
#     new_employee = forms.BooleanField(required=False, initial=False)
    

#     def clean(self):
#         cleaned = super().clean()
#         SID_or_name = cleaned.get("SID_or_name")
#         if (not SID_or_name):
#             raise forms.ValidationError("SID_or_name cannot be blank")
#         if str(SID_or_name).isnumeric():
#             SID = int(SID_or_name)
#             if len(str(SID_or_name)) != 4:
#                 raise forms.ValidationError("SID should be 4 digits")
#             else:
#                 try:
#                     employee = Employee.objects.get(SID=SID)
#                 except Employee.DoesNotExist:
#                     raise forms.ValidationError("SID does not match")
#                 except:
#                     raise forms.ValidationError("Unknown Error01")
#                 if (employee):
#                     cleaned['employee']=employee
#         else:
#             name = str(SID_or_name)
#             if len(SID_or_name) < 4:
#                 chi_name = name
#                 eng_name = ''
#             else:
#                 chi_name = ''
#                 eng_name = name
#             try:
#                 if chi_name:
#                     employee = Employee.objects.get(chi_name = name)
#                 else:
#                     employee = Employee.objects.get(eng_name = name)
#             except Employee.DoesNotExist:
#                 SID = Employee.objects.values("SID").order_by("SID").last()
#                 if SID:
#                     SID = SID['SID']
#                     SID = SID + 1
#                     employee = Employee.objects.create(SID=SID, chi_name = chi_name, eng_name = eng_name)
#                     cleaned['new_employee']=True
#                 else: raise forms.ValidationError("Unknown Error 02")
#             except:
#                 raise forms.ValidationError("Unknown Error 03")
#             cleaned['employee'] = employee
#         return cleaned

class SalaryRecordForm(forms.Form):
    pay_status_list = (
        ('N', 'N'),
        ('M', 'M'),
        ('P', 'P'),
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.TextInput(attrs={'autocomplete':"", 'class': "form-control border-0 record_amount_field", 'placeholder': "Amount?", 'autofocus':'', 'onfocus':"this.select()"}))
    hourly_rate = forms.DecimalField(max_digits=10, required=False, decimal_places=2, widget=forms.TextInput(attrs={'autocomplete':"", 'list': "employee_hourly_rates", 'class': "form-control border-0 record_hourly_rate_field", 'placeholder': "Hourly Rate?"}))
    duration = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'autocomplete':"", 'class': "form-control border-0 record_weight_field", 'placeholder': "X duration"}))
    description = forms.CharField(max_length=3000, required=False,widget=forms.Textarea(attrs={'autocomplete':"", 'class': "form-control border-0 textarea description_field", 'placeholder': "Desc?"}))
    pay_status = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'autocomplete':"", 'class': "form-control border-0 pay_status_field", 'list': 'pay_status_list'}))
    cheque_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'autocomplete':"", 'class': "form-control border-0 cheque_number_field", 'placeholder': 'Cheque Number?'}))
    
    def clean(self):
        cleaned = super().clean()
        try:
            duration = cleaned['duration']
            duration = duration.replace('_', '+')
            amount = cleaned['amount']
            hourly_rate = str(cleaned['hourly_rate'])
            if amount and (hourly_rate or duration):
                raise forms.ValidationError("Only allow either amount or hourly * duration")
            if not amount:
                if hourly_rate:
                    if not re.match(r'^\d+(\.\d+)?$', hourly_rate):
                        raise forms.ValidationError("Hourly Rate can only be numbers")
                else:
                    raise forms.ValidationError("You must enter either amount or hourly * duration")
                if duration:
                    try:
                        duration_list = str(duration).split('+')
                        total_duration = 0
                        print(duration_list)
                        for thisduration in duration_list:
                            total_duration = total_duration + float(thisduration)
                        cleaned['duration'] = ''
                        totalamount = round((total_duration * float(hourly_rate)), 2)
                        cleaned['amount'] = totalamount
                        cleaned['description'] = f"{cleaned['description']}\n (Worked {duration}) = {str(total_duration)} hours\nWorked {str(total_duration)} * ${hourly_rate} = Total ${totalamount}"
                    except Exception as e:
                        raise forms.ValidationError(f'{e}, Duration is incorrectly input.')
                else:
                    raise forms.ValidationError(f'You must enter either amount or hourly * duration')
            try:
                validateChequeNumberAndPayStatus(cleaned['cheque_number'], cleaned['pay_status'])
            except Exception as e:
                raise forms.ValidationError(e)
        except Exception as e:
            raise forms.ValidationError(e)
        return cleaned
    
class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['type', 'level', 'duration', 'price']
        widgets = {
            'type': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Violin", 'list': "type_list"}),
            'level': forms.TextInput(attrs={'class': "form-control", 'placeholder': "01/Beginner", 'list': "level_list"}),
            'duration': forms.NumberInput(attrs={'class': "form-control", 'placeholder': "045/090"}),
            'price': forms.NumberInput(attrs={'class': "form-control", 'placeholder': "400.00"})
        }

    def clean(self):
        #Validation for class input
        cleaned = super().clean()
        if len(cleaned['duration']) != 3:
            raise forms.ValidationError("duration must be in 3 digits")
        
        if str(cleaned['type'][0]).islower() or str(cleaned['type'][1]).isupper():
            raise forms.ValidationError("type should be correctly capitalized")
        
        if str(cleaned['level']).isnumeric():
            if len(cleaned['level']) != 2:
                raise forms.ValidationError("numeric level must be in 2 digits")
        else:
            if str(cleaned['level'][0]).islower() or str(cleaned['level'][1]).isupper():
                raise forms.ValidationError("level should be correctly capitalized")

def countSalary(month, status = 'A'):
    month_salaries = Salary.objects.filter(month = month).values()
    if status != 'A':
        month_salaries = month_salaries.filter(pay_status = status).values()
    salaries = []
    count = 0
    for employee in Employee.objects.all():
        pay = month_salaries.filter(employee_id = employee.SID).values('amount', 'description')
        if (pay):
            count = count + 1
        #     salaries[employee.SID] = [name, pay[0]['PID'], pay[0]['PID'], pay[0]['PID']]
        # else:
        #     salaries[employee.SID] = [name, '', '', '']
    return count

CHEQUE_TYPE = ('BOC', 'HSBC')
class PrintRecordFrom(forms.Form):
    month = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'YYMM', 'class': "form-control text-end", 'readonly': ''}))
    cheque_available = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control textarea', 'placeholder': 'ChequeType-startnum-endnum\\n'}))
    change_to_printed = forms.BooleanField(initial=(False), required=False)
    print_time = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}), required=False)

    def clean(self):
        cleaned = super().clean()
        cheque_available = cleaned['cheque_available']
        cleaned['print_time'] = timezone.now().date()
        cheque_list = cheque_available.split('\r')
        month = cleaned['month']
        errors = []
        total_cheque = 0
        for details in cheque_list:
            details = details.strip()
            details = details.split('-')
            if details[0] not in CHEQUE_TYPE:
                errors.append(forms.ValidationError(f'Cheque type must be {CHEQUE_TYPE}'))
            else:
                if len(details) != 3:
                    errors.append(forms.ValidationError(f'Cheque format is wrong'))
                else:
                    if len(details[1]) != 6 or len(details[2]) != 6:
                        errors.append(forms.ValidationError(f'Cheque number format error!'))
                    else:
                        total_cheque = total_cheque + (int(details[2]) - int(details[1])) + 1
        if len(str(cleaned['month'])) != 4:
            errors.append(forms.ValidationError("Month should be in format of YYMM"))
        else:
            tomonth = int(str(cleaned['month'])[2:])
            if tomonth < 0 or tomonth > 12:
                errors.append(forms.ValidationError("Month should within 0 to 12"))
            else:
                if total_cheque:
                    cheque_needed = countSalary(month, 'N')
                    if cheque_needed != total_cheque:
                        errors.append(forms.ValidationError(f"total cheque vailable ({total_cheque}) != total cheque needed ({cheque_needed})"))
        if errors:
            raise forms.ValidationError(errors)
        return cleaned

