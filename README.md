# AISEES database

Authors:
* Bridget Kim

Description
* Database for Balkan Academic research AISEES

Instructions
* pip install django mysqlclient
* cd myproject
* pip install -r requirements.txt
* python -m django --version
* django-admin startproject mysite (makes webpage)
* python3 manage.py runserver (runs in development server)
* python3 manage.py startapp polls (makes an app)
* python3 manage.py migrate
* add to installed_apps in settings.py
* python manage.py makemigrations add
* By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

* Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. 
* python manage.py sqlmigrate add 0001 (lets me see the sql of the models in add app)
* run migrate again

Playing with API
* python manage.py shell
* if port already in use error, netstat -ntlp, kill -9 PID
* or you can go to ports tab and kill

When you make change to models
* python3 manage.py makemigrations
* python3 manage.py migrate
* python3 manage.py runserver


email
debugging, sends it to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


real life
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your.smtp.host'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_USE_TLS = True

Ensure that EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, and other settings are correctly set for your email provider.


Refresh Mac CSS
* hold shift key while clikcing refresh icon

to select multiple things
click an item, shift click another, selects everything between those items including them

click an item ctrl (windows) cmd (mac) click another, selects only those two items, ctrl/cmd click again to unselect


python3 manage.py collectstatic before finish

unverified users have no staff permissions, can still views stuff, but can't edit stuff.
to verify click the users name and check staff, then move them into the author group, this lets them create and edit/delete the research items they uploaded
