# Lifebelt server

## [Nice deploying Django tutorial](http://adambeagle.com/blog/deploying-django-17-ubuntu/)

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

  Sensitive data such as the Django secret key, database credentials, etc. are assumed to be kept in environment variables exported and unset, respectively, by the `postactivate` and `predeactivate` scripts of the project's virtual environment. Assuming virtualenvs are kept in `/home/yournamehere/.virtualenvs`, these files are located as such:

  ```
  .virtualenvs/
    yourproject/
        bin/
            postactivate
            predeactivate
  ```

  `postactivate` might look like this:

  ```
  #!/bin/bash
  # This hook is sourced after this virtualenv is activated.

  # I mashed the keyboard; this is not a real secret key.
  export SECRET_KEY='ukh3qfu%3jh@jf('
  export DB_USERNAME=yournamehere
  export DB_PASSWORD=dbpassword
  ```

  In that case, `predeactivate` should contain:

  ```
  #!/bin/bash
  # This hook is sourced before this virtualenv is deactivated.
  unset SECRET_KEY
  unset DB_USERNAME
  unset DB_PASSWORD
  ```

  If this is new to you, note that the Django settings would access these variables like so:

  ```
  from os import environ

  SECRET_KEY = environ['SECRET_KEY']
  ```

3. Setup secrets

  Rename `local_settings.py.sample` to `local_settings.py` and edit it.

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
