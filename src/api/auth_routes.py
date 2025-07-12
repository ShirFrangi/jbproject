# built-in packages
import re

# internal packages
from src.api.utils.api_utils import is_valid_email, is_valid_password, all_fields_filled
from src.services.user_service import UserService
from src.dal.user_dao import UserDAO

# external packages
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort


bp = Blueprint('auth', __name__)

@bp.route("/login", methods=["GET", "POST"])
def login_page():
    """
    Handles user login with input validation.
    Redirects to home on successful login, else renders login form with errors.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not all_fields_filled(email, password):
            flash("נא למלא את כל השדות", category="error")
            return redirect(url_for("auth.login_page"))
        
        if not is_valid_email(email):
            flash("נא להזין כתובת אימייל חוקית", category="error")
            return redirect(url_for("auth.login_page"))

        if not is_valid_password(password):
            flash("הסיסמה חייבת להכיל לפחות 4 תווים", category="error")
            return redirect(url_for("auth.login_page"))

        try:
            user = UserService().login(email, password)
            if user:
                session.update({
                    "user_id": user.user_id,
                    "role_id": user.role_id,
                    "user_name": user.first_name
                })
                return redirect(url_for("vacations.home_page"))
            else:
                flash("אימייל או סיסמה שגויים", category="error")

        except Exception:
            abort(500)

        return redirect(url_for("auth.login_page"))
    
    # GET
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register_page():
    """
    Handles user registration with input validation.
    Redirects to home on successful registration, else renders registration form with errors.
    """
    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")

        if not all_fields_filled(first_name, last_name, email, password):
            flash("נא למלא את כל השדות", category="error")
            return redirect(url_for("auth.register_page"))

        if not is_valid_email(email):
            flash("נא להזין כתובת אימייל חוקית", category="error")
            return redirect(url_for("auth.register_page"))

        if not is_valid_password(password):
            flash("הסיסמה חייבת להכיל לפחות 4 תווים", category="error")
            return redirect(url_for("auth.register_page"))

        try:
            if UserDAO().email_exists(email):
                flash("אימייל זה כבר קיים במערכת", category="error")
                return redirect(url_for("auth.register_page"))

            user = UserService().register(first_name, last_name, email, password)
            if user:
                session.update({
                    "user_id": user.user_id,
                    "role_id": user.role_id,
                    "user_name": user.first_name
                })
                return redirect(url_for("vacations.home_page"))

        except Exception:
            abort(500)

        return redirect(url_for("auth.register_page"))
    
    # GET
    return render_template("register.html")


@bp.route("/logout")
def logout():
    """
    Clears user session and redirects to login page.
    """
    try:
        session.clear()
        return redirect(url_for("auth.login_page"))
    
    except Exception:
        abort(500)
        
#
