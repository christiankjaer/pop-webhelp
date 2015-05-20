from functools import wraps
from flask import abort
from flask_login import current_user

def role_must_be(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role == role:
                return f(*args, **kwargs)
            else:
                return abort(401)
        return decorated_function
    return decorator
