Code for initializing MySQL

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
ALTER USER 'root'@'localhost' IDENTITIFIED WITH auth_socket;
CREATE USER 'mushroomsqluser'@'%' IDENTIFIED BY 'password';
CREATE USER 'mushroomsqluser'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE mushroom;
GRANT ALL PRIVILEGES ON mushroom._ TO 'mushroomsqluser'@'%';
GRANT ALL PRIVILEGES ON mushroom._ TO 'mushroomsqluser'@'localhost';
