### Test task

---


*Brief introduction*

Assume that you're developing an app for an existing Django project. The app should
introduce an **"Alias"** object/model, defined as such:
- "alias" field - string (no specific requirements)
- "target" field - string (a "soft foreign key" to slugs of other models/apps of the existing
project; will never be longer than 24 characters)
- "start" field - microsecond precision timestamp/datetime
- "end" field - microsecond precision timestamp/datetime or None

- - - 


This project should be launched(the development server and the test suite):


```
python manage.py runserver
python manage.py test
```
