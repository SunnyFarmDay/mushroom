
from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = "SalaryInput"
urlpatterns = [
    path('home/', views.home),
    path('', lambda request: redirect('/home', permanent=True)),
    path('salary/month/<str:month>', views.monthSalary),
    path('salary_input/', views.salaryInput, name="salary_input"),
    path('class_input/', views.classInput, name="class_input"),
    path('export_classes_csv', views.exportClassesToCSV, name="export_classes_csv")
]
