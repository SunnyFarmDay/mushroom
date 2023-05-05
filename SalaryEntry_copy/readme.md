#Launching web server:

1. create venv with
   '''
   python -m venv venv
   '''
2. Migrate for the database
   '''
   python EmployeeSystem/manage.py migrate
   '''
3. Run the web server
   '''
   python EmployeeSystem/manage.py runserver localhost:8000
   '''
