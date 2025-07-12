# built-in packages
import re
from functools import wraps

# external packages
from flask import session, redirect, url_for, abort


def admin_required(f):
    """
    Decorator: Ensures the user is an admin.
    Aborts with 403 if not.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role_id") != 2:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """
    Decorator: Ensures the user is logged in.
    Redirects to login page if not.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)
    return decorated_function


def all_fields_filled(*fields) -> bool:
    """
    Checks if all provided fields are non-empty.
    Returns True if all fields are truthy.
    """
    return all(fields)


def is_valid_email(email: str) -> bool:
    """
    Checks if the given email address is in a valid format.
    Returns True if valid.
    """
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def is_valid_password(password: str, min_length: int = 4) -> bool:
    """
    Checks if the password meets minimum length.
    Returns True if valid.
    """
    return len(password) >= min_length

#
