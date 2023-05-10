#Launching web server:

Prerequisite:
Installed docker-compose

1. cd DjangoProject

2. run docker-compose up --build

3. access the server via localhost

#WSL network mapping
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=80 connectaddress=172.21.224.1
