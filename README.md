# AISEES database

Authors:
* Bridget Kim

Description
* Database for Balkan Academic research AISEES

How Admin Access Works
* When you register to make an account, you cannot sign in until you verify your email
* users start off with no staff permissions, can still view stuff, but can't edit stuff.
* to make user able to add to database and edit their additions:
	* Admin goes to account page
	* Go to user page
	* Click on user
	* check staff permissions, this lets them access account page
	* then move them into the author group, this lets them create and edit/delete the research items they uploaded

Instructions on Django
```c
pip3 install git
git clone https://github.com/lommoberry/AISEES.git
cd AISEES
pip3 install django mysqlclient
cd myproject
pip3 install -r requirements.txt
python3 -m django --version
django-admin startproject mysite (makes webpage)
python3 manage.py runserver (runs in development server)
python3 manage.py startapp polls (makes an app)
python3 manage.py migrate
add to installed_apps in settings.py
python3 manage.py makemigrations add
```

* By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

* Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. 
* python manage.py sqlmigrate add 0001 (lets me see the sql of the models in add app)
* run migrate again


Playing with API
* if port already in use error, 
```c
netstat -ntlp
kill -9 PID
```

When you make change to models
```c
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

Notes
* email
	* debugging, sends it to console
		* EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


	* real life
		* EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
		* EMAIL_HOST = 'your.smtp.host'
		* EMAIL_PORT = 587
		* EMAIL_HOST_USER = 'your-email@example.com' (change to host email)
		* EMAIL_HOST_PASSWORD = 'yourpassword' (if gmail, go to appspassword and add new)
		* EMAIL_USE_TLS = True

	* Ensure that EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, and other settings are correctly set for your email provider.


* Refresh Mac CSS
	* hold shift key while clikcing refresh icon

* to select multiple things
	* click an item, shift click another, selects everything between those items including them

	* click an item ctrl (windows) cmd (mac) click another, selects only those two items, ctrl/cmd click again to unselect

Finishing Up
* when you are done, collect static collects all your static files, like formatting, images, etc. Puts them all into one folder.

```c
python3 manage.py collectstatic 
```
