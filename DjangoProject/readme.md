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

#WSL network mapping
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=80 connectaddress=172.21.224.1
