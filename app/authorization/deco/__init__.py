from functools import wraps
from flask_login import current_user
from flask import render_template

def admin_req(f):
    @wraps(f)
    def deco_function(*args, **kwargs):
        if current_user.is_admin != 1:
            return render_template('403.html'), 403
        return f(*args, **kwargs)
    return deco_function