from functools import wraps

from flask import abort
from flask.ext.login import current_user


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated() and current_user.get_role() not in roles:
                abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
