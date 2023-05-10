from django.shortcuts import render, redirect
from .models import Salary, Employee, Class
from .forms import SalaryRecordForm, CreateClassForm, EmployeeSalarySelectionForm, PrintRecordFrom, countSalary
from datetime import datetime
from django.forms import formset_factory
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
import numpy as np
from .print import print_record
# Create your views here.

#Get namelist
def getEmployeesName():
    Employees = Employee.objects.all()
    names = []
    for employee in Employees:
        if employee.chi_name:
            names.append(employee.chi_name)
        else:
            names.append(employee.eng_name)
    return names

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

def monthSalary(request, month, status):
    context = getContext()
    context['month_salaries'] = getMonthSalary(month, status, merged=False)
    print(getMonthSalary(month, status, merged=False))
    context['month']=month
    context['record_form_open']='False'
    cheque_needed = countSalary(month, 'N')
    context['cheque_needed'] = cheque_needed
    print_record_form = PrintRecordFrom(initial=({'month': month}))
    context['print_record_form'] = print_record_form
    if request.method == 'POST':
        print('post')
        action = str(request.POST.get('action')).split('-')
        print(action)
        if action[0] == 'print_record_form':
            form = PrintRecordFrom(request.POST)
            if form.is_valid():
                print('valid')
                cleaned = form.cleaned_data # {'month': 2304, 'cheque_available': 'BOC-100001-100030', 'change_to_printed': True, 'print_time': datetime.date(2023, 5, 7)}
                print(cleaned)
                cheques = cleaned['cheque_available']
                details = str(cheques).split('\r')
                cheque_available = []
                for detail in details:
                    detail = detail.strip().split('-')
                    for i in range(int(detail[1]), int(detail[2])+1):
                        cheque_available.append([detail[0], str(i)])
                salary_record = getMonthSalary(month, 'N', description=True)
                if (cleaned['change_to_printed']):
                    employees = Employee.objects.all()
                    count = 0
                    for employee in employees:
                        salaries = Salary.objects.filter(employee = employee, month = month, pay_status = 'N')
                        if (salaries):
                            for salary in salaries:
                                Salary.objects.filter(PID = salary.PID).update(paid_time = cleaned['print_time'], pay_status = 'P', cheque_number = f"{cheque_available[count][0]}-{cheque_available[count][1]}")
                                print(salary, salary.paid_time, salary.pay_status, salary.cheque_number)
                            count = count + 1
                return printRecord(cheque_available, month, salary_record)
            else:
                context['print_record_form'] = PrintRecordFrom(request.POST)
                context['record_form_open']='True'
                print('error')
    return render(request, 'MonthSalaries.html', context)

def getMonthSalary(month, status, description = True, merged=True):
    month_salaries = Salary.objects.filter(month = month).values()
    if status != 'A':
        month_salaries = month_salaries.filter(pay_status = status).values()
    salaries = []
    if merged:
        for employee in Employee.objects.all():
            pay = month_salaries.filter(employee_id = employee.SID).values('amount', 'description')
            salary = []
            if ( employee.chi_name):
                name = employee.chi_name
            else:
                name = employee.eng_name
            salary.append(employee.SID)
            salary.append(name)
            if (pay):
                amount = 0
                descriptions = ''
                for thispay in pay:
                    amount = thispay['amount'] + amount
                    if thispay['description']:
                        descriptions = descriptions +'___' + thispay['description']
                salary.append(amount)
                if description:
                    salary.append(descriptions.replace('\n', '_'))
            salaries.append(salary)
            # if (pay):
            #     salaries[employee.SID] = [name, pay[0]['PID'], pay[0]['PID'], pay[0]['PID']]
            # else:
            #     salaries[employee.SID] = [name, '', '', '']
    else:
        salaries = []
        for employee in Employee.objects.all():
            pays = month_salaries.filter(employee_id = employee.SID).values()
            if employee.chi_name:
                name = employee.chi_name
            else:
                name = employee.eng_name
            if pays:
                total = 0
                details = []
                pay_status = {'N': 0, 'P': 0, 'M': 0}
                for pay in pays:
                    total = pay['amount'] + total
                    # pay['SID'] = employee.SID
                    # pay['name'] = name
                    details.append(pay['pay_status'])
                    if pay_status[pay['pay_status']]:
                        pay_status[pay['pay_status']] = pay_status[pay['pay_status']] + 1
                    else:
                        pay_status[pay['pay_status']] = 1
                p = pay_status['P']
                t = pay_status['N'] + pay_status['M'] + pay_status['P']
                if t != p:
                    pay_status = f'{p} out of {t} Printed'
                else:
                    pay_status = 'Printed'
                salaries.append({
                'SID': employee.SID,
                'name': name,
                'amount': total,
                'details': details,
                'pay_status': pay_status
            })
            else:
                salaries.append({
                    'SID': employee.SID,
                    'name': name,
                })
    return salaries

def employeeSalaryInput(request, SID, month):
    context = getContext()
    employee = Employee.objects.get(SID = SID)
    context['month'] = month
    context['employee_SID'] = employee.SID
    context['employee_chi_name'] = employee.chi_name
    context['employee_eng_name'] = employee.eng_name
    SelectionForm = EmployeeSalarySelectionForm(initial={'month': month})
    context['selection_form'] = SelectionForm
    context['Employees_name'] = getEmployeesName()
    #generate the record creation form
    SalaryRecordFormSet = formset_factory(SalaryRecordForm, extra=0)
    formset = SalaryRecordFormSet(initial =[
        {'pay_status': 'N', 'month': month}
    ])
    context['formset'] = formset
    if request.method == 'POST':
        print('post')
        action = (request.POST.get('action')).split('-')
        if action[0] == 'selection_form':
            SelectionForm = EmployeeSalarySelectionForm(request.POST)
            if SelectionForm.is_valid():
                cleaned = SelectionForm.cleaned_data
                month = cleaned['month']
                context['month'] = month
                context['selection_form'] = SelectionForm
                #if employee is selected 
                if (cleaned['new_employee'] == True):
                    messages.add_message(request, messages.SUCCESS, f"New Employee with SID {cleaned['employee'].SID} created.")
                return redirect(f"/salary_input/{cleaned['employee'].SID}/{month}")
            else:
                context['selection_form'] = SelectionForm
                print('error')
        
        elif action[0] == 'add_record':
            formset = SalaryRecordFormSet(request.POST)
            print('add_record')
            print(formset.errors)
            for thisform in formset:
                if thisform.is_valid():
                    print('valid')
                    cleaned = thisform.cleaned_data
                    amount = cleaned['amount']
                    description = cleaned['description']
                    pay_status = cleaned['pay_status']
                    salary = Salary.objects.create(employee = employee, month = month, amount = amount, description = description, pay_status = pay_status)
                    messages.success(request, f"New Salary with PID {salary.PID} created.")
                else:
                    print('error')
                    context['formset'] = formset
                    for errors in formset.errors:
                        for key, value in errors.items():
                            for thiserror in value:
                                print(thiserror)
                                messages.error(request, f"Input {key}: {thiserror}")
        elif action[0] == 'delete':
            PID = action[1]
            salary = Salary.objects.get(PID=PID)
            salary.delete()
            
            messages.info(request, f"Salary with PID {PID} has been deleted.")
        
    else:
        print('get')
    records = Salary.objects.filter(employee = employee, month = month).values()
    print(records)
    total = 0
    for salary in records:
        total = total + salary['amount']
    context['total'] = total
    context['SalaryRecords'] = records
    return render(request, "SalaryInput.html", context)




def salaryInput(request):

    month = str(int(datetime.now().strftime("%Y%m")[2:]) - 1) #temp solution for changing month to previous
    context = getContext()

    #Add datalist for Employees' name choices
    context['Employees_name'] = getEmployeesName()

    if request.method == 'POST':
        print('post')
        action = request.POST['action'].split('-')
        if action[0] == 'selection_form':
            SelectionForm = EmployeeSalarySelectionForm(request.POST)
            if SelectionForm.is_valid():
                cleaned = SelectionForm.cleaned_data
                month = cleaned['month']
                context['month'] = month
                context['selection_form'] = SelectionForm
                #if employee is selected 
                if (cleaned['new_employee'] == True):
                    messages.add_message(request, messages.SUCCESS, f"New Employee with SID {cleaned['employee'].SID} created.")
                return redirect(f"/salary_input/{cleaned['employee'].SID}/{month}")
            else:
                context['selection_form'] = SelectionForm
                print('error')
            #get all employee's salary records
    else:
        print('get')
        SelectionForm = EmployeeSalarySelectionForm(initial={'month': month})
        context['selection_form'] = SelectionForm
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

def exportMonthlySalaryToCSV(request, month, status):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Salary-{month}-{datetime.now().strftime("%Y%m%d-%X")}.csv"'
    df = pd.DataFrame(getMonthSalary(month, status, description=True))
    print(df)
    df = df.set_axis(["SID", "name", "salary", "description"], axis='columns')
    print(df)
    df.to_csv(path_or_buf=response, encoding='utf_8_sig', index=False) # type: ignore
    return response

def printRecordPDF(request, month):
    date = {
        'day': '7',
        'month': month[2:],
        'year': f'20{month[:2]}'
    }
    df = pd.DataFrame(getMonthSalary(month, 'N', description=True))
    df = df.set_axis(["SID", "name", "amount", "description"], axis='columns')
    data = []
    for _, row in df.iterrows():
        if row['amount']:
            row_data = {}
            row_data['layout'] = 'BOC'
            row_data['SID'] = row['SID']
            row_data['name'] = row['name']
            row_data['amount'] = row['amount']
            row_data['description'] = row['description']
            data.append(row_data)
    file = print_record(date, data)
    with open(file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Cheque-BOC-{month}-{datetime.now().strftime("%Y%m%d-%X")}.pdf"'
    f.close()
    return response

def printRecord(cheque_available, month, salary_record):
    date = {
        'day': '7',
        'month': month[2:],
        'year': f'20{month[:2]}'
    }
    df = pd.DataFrame(salary_record)
    df = df.set_axis(["SID", "name", "amount", "description"], axis='columns')
    data = []
    count = 0
    for _, row in df.iterrows():
        if row['amount']:
            row_data = {}
            row_data['layout'] = cheque_available[count][0]
            row_data['cheque_number'] = cheque_available[count][1]
            row_data['SID'] = str(row['SID'])
            row_data['name'] = row['name']
            row_data['amount'] = row['amount']
            row_data['description'] = row['description']
            data.append(row_data)
            count = count + 1
    file = print_record(date, data)
    with open(file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Cheque-BOC-{month}-{datetime.now().strftime("%Y%m%d-%X")}.pdf"'
    f.close()
    return response

