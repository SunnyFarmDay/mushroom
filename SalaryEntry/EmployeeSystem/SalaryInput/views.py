from django.shortcuts import render
from .models import Salary, Employee
from .forms import SalaryRecordForm
from datetime import datetime
from django.forms import formset_factory

# Create your views here.
def getContext():
    context ={}
    months = []
    for month in Salary.objects.values('month').distinct():
        months.append(month['month'])
    context["salary_months"] = months
    return context
def home(request):
    context = getContext()
    return render(request, 'Home.html', context)

def monthSalary(request, month):
    context = getContext()
    context['month_salaries'] = getMonthSalary(month)
    return render(request, 'MonthSalaries.html', context)

def getMonthSalary(month):
    month_salaries = Salary.objects.filter(month = month).values()
    salaries = []
    # for salary in month_salaries:
    #     employee = Employee.objects.get(SID = salary['employee_id'])
    #     if (employee.chi_name):
    #         name = employee.chi_name
    #     else:
    #         name = employee.eng_name
    #     thispay = [salary['pid'], name, str(salary['amount']), salary['description']]
    #     salaries.append(thispay)
    
    for employee in Employee.objects.all():
        pay = month_salaries.filter(employee_id = employee.SID).values('amount', 'description')
        print(pay)
        name = employee.chi_name
        if (not employee.chi_name):
            name = employee.eng_name
        if (pay):
            salaries.append([employee.SID, name, pay[0]['amount'], pay[0]['description']])
        else:
            salaries.append([employee.SID, name, '', ''])
        # if (pay):
        #     salaries[employee.SID] = [name, pay[0]['pid'], pay[0]['pid'], pay[0]['pid']]
        # else:
        #     salaries[employee.SID] = [name, '', '', '']
    return salaries

def salaryInput(request):
    if ('month' in request.GET):
        month = request.GET.get('month')
    else:
        month = datetime.now().strftime("%Y%m")[2:]
    print(month)
    context = getContext()
    context['month'] = month
    SalaryRecordFormSet = formset_factory(SalaryRecordForm, extra=0)
    formset = SalaryRecordFormSet(initial =[
        {'pay_status': 'N', 'month': month}
    ])
    context['forms'] = formset
    
    if request.method == 'POST':
        print('post')
        formset = SalaryRecordFormSet(request.POST)
        print(formset)
        for thisform in formset:
            if thisform.is_valid():
                print('valid')
                cleaned = thisform.clean()
                try:
                    salary = Salary.objects.create(employee = cleaned['employee'], month=month, amount=cleaned['amount'], description=cleaned['description'], pay_status=cleaned['pay_status'])
                except:
                    context['error'] = "Salary already exist"
                    return render(request, "SalaryInput.html", context)
                print(salary)
            else:
                context['forms'] = formset
                print('error')
        return render(request, "SalaryInput.html", context)
    else:
        print('get')
        return render(request, "SalaryInput.html", context)
