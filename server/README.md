# Lifebelt server

## Configure and run

1. Edit `lifebelt/settings/__init__.py`

  Add all needed secret information like keys, passwords etc...

2. Make migrations

  `python manage.py migrate`

3. Create superuser

  `python manage.py createsuperuser` and follow the instructions

3. Run server

  `python manage.py runserver`

And that's it! Now open your browser login and you have access to Lifebelt's Browsable API

## Available APIs list

For full list take a look on our API blueprint
