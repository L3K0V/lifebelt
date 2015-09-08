# Lifebelt server

## Configure and run

1. Make sure you have installed Python3
2. Setup virtual environment and install `requirements.txt`
  
  ```
  $ cd lifebelt/server
  $ python3 virtualenv env
  
  $ source env/bin/activate
  $ pip install requirements.txt
  ```

3. Setup secrets

  Rename local_settings.py.sample to local_settings.py and edit it.

4. Make migrations

  ```
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```

5. Create superuser

  `$ python manage.py createsuperuser` and follow the instructions

6. Run server

  `$ python manage.py runserver`

And that's it! Now open your browser login and you have access to Lifebelt's Browsable API

## Available APIs list

For full list take a look on our API blueprint
