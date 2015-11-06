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

3. Setup server secrets

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

  # Lifeblet's github id and secret
  export LIFEBELT_GITHUB_CLIENT_ID=
  export LIFEBELT_GITHUB_CLIENT_SECRET=

  # Lifebelt's bot access token
  export LIFEBELT_BOT_TOKEN=

  # Email address used and password for password recovery and some other cool stuff
  export EMAIL_HOST_USER=
  export ÒEMAIL_HOST_PASSWORD
  ```

  In that case, `predeactivate` should contain:

  ```
  #!/bin/bash
  # This hook is sourced before this virtualenv is deactivated.
  unset SECRET_KEY
  unset DB_USERNAME
  unset DB_PASSWORD

  unset LIFEBELT_GITHUB_CLIENT_ID
  unset LIFEBELT_GITHUB_CLIENT_SECRET

  unset LIFEBELT_BOT_TOKEN

  unset EMAIL_HOST_USER
  unset EMAIL_HOST_PASSWORD
  ```

  If this is new to you, note that the Django settings would access these variables like so:

  ```
  from os import environ

  SECRET_KEY = environ['SECRET_KEY']
  ```

4. Make migrations

  ```
  # From the project root directory
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```

5. Create superuser

  ```
  # From the project root directory
  $ python manage.py createsuperuser
  ```

  and follow the instructions

6. Run server

  `$ python manage.py runserver`
  `$ python manage.py celery -A lifebelt worker --loglevel=info`

And that's it! Now open your browser login and you have access to Lifebelt's Browsable API

## Production deploying

1. Collect static

  ```
  python manage.py collectstatic --settings=yourproject.settings.production
  ```
