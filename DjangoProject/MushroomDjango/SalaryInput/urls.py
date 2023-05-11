
from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = "SalaryInput"
urlpatterns = [
    path('home/', views.home),
    path('', lambda request: redirect('/home', permanent=True)),
    path('salary/month/<str:month>/<str:status>', views.monthSalary, name='monthly_salary'),
    path('salary_input/', views.salaryInput, name="salary_input"),
    path('salary_input/<int:SID>/<int:month>', views.employeeSalaryInput, name="employee_salary_input"),
    path('class_input/', views.classInput, name="class_input"),
    path('export_classes_csv', views.exportClassesToCSV, name="export_classes_csv"),
    path('export_monthly_salary_csv/<int:month>/<str:status>', views.exportMonthlySalaryToCSV, name="export_monthly_salary_csv"),
    path('print_record_pdf/<str:month>', views.printRecordPDF, name='print_record_pdf')
]