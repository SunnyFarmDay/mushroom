from django.shortcuts import render
from .models import Salary, Employee, Class
from .forms import SalaryRecordForm, CreateClassForm
from datetime import datetime
from django.forms import formset_factory
from django.contrib import messages
from django.core import management
import csv
from django.http import HttpResponse
import pandas as pd
# Create your views here.

#Get default context (Salary)
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
    #     thispay = [salary['PID'], name, str(salary['amount']), salary['description']]
    #     salaries.append(thispay)
    
    for employee in Employee.objects.all():
        pay = month_salaries.filter(employee_id = employee.SID).values('amount', 'description')
        print(pay)
        if ( employee.chi_name):
            name = employee.chi_name
        else:
            name = employee.eng_name
        if (pay):
            amount = 0
            description = ''
            for thispay in pay:
                amount = thispay['amount'] + amount
                if thispay['description']:
                    description = description +'\n' + thispay['description']
            salaries.append([employee.SID, name, amount, description])
        else:
            salaries.append([employee.SID, name, '', ''])
        # if (pay):
        #     salaries[employee.SID] = [name, pay[0]['PID'], pay[0]['PID'], pay[0]['PID']]
        # else:
        #     salaries[employee.SID] = [name, '', '', '']
    return salaries

def salaryInput(request):
    if ('month' in request.GET):
        month = request.GET.get('month')
    else:
        month = str(int(datetime.now().strftime("%Y%m")[2:]) - 1) #temp solution for changing month to previous
    print(month)
    context = getContext()
    context['month'] = month

    #Add datalist for Employees' name choices
    Employees = Employee.objects.all().values()
    names = []
    for employee in Employees:
        if employee['chi_name']:
            names.append(employee['chi_name'])
        else:
            names.append(employee['eng_name'])
    context['Employees_name'] = names
    SalaryRecordFormSet = formset_factory(SalaryRecordForm, extra=0)
    formset = SalaryRecordFormSet(initial =[
        {'pay_status': 'N', 'month': month}
    ])
    context['forms'] = formset
    if request.method == 'POST':
        print('post')
        formset = SalaryRecordFormSet(request.POST)
        for thisform in formset:
            print(thisform['employee'])
            if thisform.is_valid():
                thisform=thisform.clean()
                if (thisform['new_employee'] == True):
                    messages.add_message(request, messages.SUCCESS, f"New Employee with SID {thisform['employee'].SID} created.")
                try:
                    salary = Salary.objects.create(employee = thisform['employee'], month=month, amount=thisform['amount'], description=thisform['description'], pay_status=thisform['pay_status'])
                    messages.add_message(request, messages.SUCCESS, f"New salary record with PID {salary.PID} created.")
                    print(salary)
                    print('valid')
                except Exception as e:
                    messages.add_message(request, messages.ERROR, f"{e}!")
            else:
                print('error')
            
        context['forms'] = formset
        return render(request, "SalaryInput.html", context)
    else:
        print('get')
        return render(request, "SalaryInput.html", context)

### old
# def salaryInput(request):
#     if ('month' in request.GET):
#         month = request.GET.get('month')
#     else:
#         month = str(int(datetime.now().strftime("%Y%m")[2:]) - 1) #temp solution for changing month to previous
#     print(month)
#     context = getContext()
#     context['month'] = month

#     #Add datalist for Employees' name choices
#     Employees = Employee.objects.all().values()
#     names = []
#     for employee in Employees:
#         if employee['chi_name']:
#             names.append(employee['chi_name'])
#         else:
#             names.append(employee['eng_name'])
#     context['Employees_name'] = names
#     SalaryRecordFormSet = formset_factory(SalaryRecordForm, extra=0)
#     formset = SalaryRecordFormSet(initial =[
#         {'pay_status': 'N', 'month': month}
#     ])
#     context['forms'] = formset
#     if request.method == 'POST':
#         print('post')
#         formset = SalaryRecordFormSet(request.POST)
#         for thisform in formset:
#             print(thisform['employee'])
#             if thisform.is_valid():
#                 thisform=thisform.clean()
#                 if (thisform['new_employee'] == True):
#                     messages.add_message(request, messages.SUCCESS, f"New Employee with SID {thisform['employee'].SID} created.")
#                 try:
#                     salary = Salary.objects.create(employee = thisform['employee'], month=month, amount=thisform['amount'], description=thisform['description'], pay_status=thisform['pay_status'])
#                     messages.add_message(request, messages.SUCCESS, f"New salary record with PID {salary.PID} created.")
#                     print(salary)
#                     print('valid')
#                 except Exception as e:
#                     salary = Salary.objects.get(employee = thisform['employee'], month=month)
#                     PID = salary.PID
#                     old_amount = salary.amount
#                     amount = thisform['amount']
#                     salary.amount = amount
#                     salary.save()
#                     messages.add_message(request, messages.INFO, f"Salary #{PID} amount updated from {old_amount} to {amount}!")
#             else:
#                 print('error')
            
#         context['forms'] = formset
#         return render(request, "SalaryInput.html", context)
#     else:
#         print('get')
#         return render(request, "SalaryInput.html", context)


type_list = ['Violin', 'Piano', 'Theory', 'Ukulele', 'Guitar', 'Bass', 'Harp', 'Tutorial', 'Art']
level_list = ['01', '02', '03', '04', '05', '06', '07', '08', 'Beginner', 'Intermediate', 'Advanced']

def classInput(request):
    context = getContext()
    form = CreateClassForm(request.POST)
    context['type_list'] = type_list
    context['level_list'] = level_list
    if request.method == 'POST':
        print(request.POST.get('action'))
        if request.POST['action'] == "class_edit":
            if form.is_valid():
                newClass = form.save()
                messages.add_message(request, messages.SUCCESS, f"New class with {newClass.CID} created.")
            else:
                messages.add_message(request, messages.ERROR, f"Error in creating class.")
                pass
            
        else:
            form = CreateClassForm()
            action = request.POST['action'].split('-')
            if action[0] == "delete":
                CID = action[1]
                try:
                    theClass = Class.objects.get(CID = CID)
                    theClass.delete()
                    messages.add_message(request, messages.INFO, f"Class {CID} has been deleted!")
                except:
                    messages.add_message(request, messages.ERROR, f"Class {CID} does not exist!")

            
    else:
        form = CreateClassForm()
    context['form'] = form
    context['Classes'] = Class.objects.all()
    return render(request, 'ClassInput.html', context)

def exportClassesToCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Classes-{datetime.now().strftime("%Y%m%d-%X")}.csv"'
    # writer = csv.writer(response)
    # writer.writerow(['CID', 'type', 'level', 'duration', 'price'])
    # Classes = Class.objects.all().values()
    # print(Classes)
    # for theClass in Classes:
    #     theClass['price'] = str(theClass['price'])
    # for theClass in Classes:
    #     print(theClass.values())
    #     writer.writerow(theClass.values())
    # return response
    df = pd.DataFrame(Class.objects.all().values())
    csv = df.to_csv(path_or_buf=response, index=False) # type: ignore
    print(csv)
    return response