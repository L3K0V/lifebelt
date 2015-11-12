# Lifebelt server

## [Nice deploying Django tutorial](http://adambeagle.com/blog/deploying-django-17-ubuntu/)

## Requirements

Requires Python 3.+

Rest of the requirements should be installed from `requirements.txt` using `pip`.

For local development the easy way is to use SQLite database, but for deployment
configuration must be switched to use PostgreSQL.

## Installation and configuration

1. Setup virtual environment using `virtualenv` or `virtualenvwrapper`
  ```
  $ cd <path-to-project>/server

  # if using virtualenv
  $ python3 virtualenv env

  # or using wrapper
  $ python3 mkvirtualenv lifebelt
  ```

2. Activate newly created virtual environment

  ```
  # if using virtualenv execute from directory where is the env
  $ source env/bin/activate

  # or using wrapper
  $ workon lifebelt
  ```

3. Install dependencies

  ```
  $ pip install --upgrade pip
  $ pip install -r requirements.txt
  ```

4. Setup server secrets

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
  export EMAIL_HOST_PASSWORD

  # Used both for Django and celery
  export DJANGO_SETTINGS_MODULE=lifebelt.settings.local
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

  unset DJANGO_SETTINGS_MODULE
  ```

  If this is new to you, note that the Django settings would access these variables like so:

  ```
  from os import environ

  SECRET_KEY = environ['SECRET_KEY']
  ```

5. Make migrations

  ```
  # From the project root directory

  # Notice that migrations are in the source control, so you can skip making them again
  $ python manage.py makemigrations
  $ python manage.py migrate
  ```

6. Create superuser

  ```
  # From the project root directory
  $ python manage.py createsuperuser
  ```

  and follow the instructions

6. Run server

  `$ python manage.py runserver`
  `$ python manage.py celery -A lifebelt worker --loglevel=info`

  And that's it! Now open your browser login and you have access to Lifebelt's Browsable API

7. Important

  - To use full functionality of Lifebelt you must setup Member profile. Member profiles extend default Django user profiles and provide to Lifebelt required GitHub and course details.

  - Configure Lifebelt Bot access to GitHub by creating member profile and fill all fields. They are needed for right behavior on submission reviewing.

  - Configure email host password etc. in settings to enable sending email to members for important actions like enrollment for course of forgotten password.

## Production deploying

1. Collect static

  ```
  python manage.py collectstatic --settings=yourproject.settings.production
  ```

(not ready yet)
