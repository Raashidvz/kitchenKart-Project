1. First create a superuser for adding manager and kitchen staff

2. Open Admin panel -> login (superuser) -> create 2 users (manager and kitchen1)


Admin Panel:
URL: http://127.0.0.1:8000/admin/
Login as superuser

Then create users ->

Manager (user1)
Username: manager
Password: 

Kitchen (user2)
Username: kitchen1
Password: 

(Passwords can be any)


--------------------------------
MYSQL Database

database name : kitchenkart_db


1. Extract zip file

2. Open in VScode

3. Open command prompt and run:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py shell < seed.py
	python manage.py runserver

   It will print :
	Manager user created
	Kitchen user created
	Sample menu items added

4. Now login as manager and kitchen

______Manager login_____
username : manager
password : kitchenmanager1234

______Kitchen staff login______
username : kitchen1
password : kitchenstaff1234













