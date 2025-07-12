# external packages
from flask import Blueprint, render_template

bp = Blueprint("errors", __name__)

@bp.app_errorhandler(400)
def bad_request(e):
    return render_template("error.html", status_code=400), 400

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("error.html", status_code=404), 404

@bp.app_errorhandler(500)
def internal_error(e):
    return render_template("error.html", status_code=500), 500

@bp.app_errorhandler(Exception)
def generic_error(e):
    return render_template("error.html", status_code=500), 500

#
