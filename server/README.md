Run applicaion using uWSGI container:

``` 
uwsgi --http-socket :3031 --plugin python --wsgi-file wsgi.py --callable app -H /path/to/virtualenv
```
