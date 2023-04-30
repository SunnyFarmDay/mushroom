from django import forms
from .models import Salary, Employee

class SalaryRecordForm(forms.Form):
    pay_status_choices = (
        ('N', 'N'),
        ('M', 'M'),
        ('P', 'P'),
    )
    SID_or_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'SID or Name', 'class': "form-control", 'aria-label':"SID_or_name", 'aria-describedby':"SID_or_name"}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': "form-control amount_field"}))
    description = forms.CharField(max_length=3000, required=False,widget=forms.Textarea(attrs={'class': "form-control textarea", 'placeholder': "*description"}))
    pay_status = forms.ChoiceField(choices = pay_status_choices, widget=forms.Select(attrs={'class': "form-control"}))
    employee = forms.ModelChoiceField(Employee.objects.all(), required=False)
    

    def clean(self):
        cleaned = super().clean()
        SID_or_name = cleaned.get("SID_or_name")
        if (not SID_or_name):
            raise forms.ValidationError("SID_or_name cannot be blank")
        if str(SID_or_name).isnumeric():
            SID = int(SID_or_name)
            if len(str(SID_or_name)) != 4:
                raise forms.ValidationError("SID should be 4 digits")
            else:
                try:
                    employee = Employee.objects.get(SID=SID)
                except Employee.DoesNotExist:
                    raise forms.ValidationError("SID does not match")
                except:
                    raise forms.ValidationError("Unknown Error01")
                if (employee):
                    cleaned['employee']=employee
        else:
            name = str(SID_or_name)
            if len(SID_or_name) >= 4:
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
            except Employee.DoesNotExist:
                SID = Employee.objects.values("SID").order_by("SID").last()
                if SID:
                    SID = SID['SID']
                    SID = SID + 1
                    employee = Employee.objects.create(SID=SID, chi_name = chi_name, eng_name = eng_name)
                else: raise forms.ValidationError("Unknown Error 02")
            except:
                raise forms.ValidationError("Unknown Error 03")
            cleaned['employee'] = employee
        return cleaned

