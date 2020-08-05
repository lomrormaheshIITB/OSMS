1. Setting up postgres database:
	The following commands are to be run in the postgres terminal.

	Set up the postgres service on your machine with host 
	as localhost and port as 5310.

	I. Create a user 'labuser' with superuser and login rights
		create role labuser with superuser login;

	II. Create a database 'osms' and grant rights to'labuser'
		create database osms;
		grant all on database osms to labuser;

	III. Login to database 'osms' using 'labuser'
		psql -h localhost -p 5310 -U labuser osms

	IV. Press Ctrl+D to logout of the psql window


The following commands are to be run in a virtual environment with
the specified versions of python and django. 
Version:
	Python - 3.6.9
	Django - 3.0.4

2. Importing the models from django into the database

	python3 manage.py makemigrations
	python3 manage.py migrate

	
3. Importing the excel file into the database
	
	cd db
	python excel_to_db.py --file OSMS \FINAL_EXCEL_SHEET_TEMPLATE.xlsx \
	cd ..

4. Creating a superuser

	python3 manage.py createsuperuser
	Enter the following details:
		Username: admin
		Firstname: admin
		Lastname: admin
		Rank: LT
		Personal number: 123
		Section: abc
		Can edit: True
		Password: 123
		Password (again): 123
		Type 'y' when prompted and press Enter.


5. Run server
	
	python3 manage.py runserver
	Open 127.0.0.1:8000 on a web browser.
