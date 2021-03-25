# Finance Tracker
###### a django web application to track your finances

Currently this is a simple web application to track your finances.
Features include:
- Logging transactions
- Logging gains
- Logging a borrow
- Logging a lend
- Creating and tracking your balances
- Creating new classifications for your transactions
- User system with django authentication
- Charts made with charts.js
- Deleting transactions and balances



__Requirements:__
```
pip install django
```

__To run the application:__
Run these just in case
```
py manage.py makemigrations
py manage.py migrate
```
Create yourself a superuser
```
py manage.py createsuperuser
```
Run the app
```
py manage.py runserver
```
the now running application can be access via __localhost:8000__

