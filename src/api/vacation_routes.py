# built-in packages
from datetime import datetime
import os

# internal packages
from src.config import UPLOAD_FOLDER
from src.api.utils.api_utils import admin_required, login_required, all_fields_filled
from src.dal.vacation_dao import VacationDAO
from src.dal.country_dao import CountryDAO
from src.dal.like_dao import LikeDAO
from src.services.vacation_service import VacationService
from src.services.user_service import UserService

# external packages
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, abort
from werkzeug.utils import secure_filename


bp = Blueprint('vacations', __name__)


@bp.route("/")
@login_required
def home_page():
    """
    Renders the home page with all vacations and user-specific data.
    Redirects to login if the user is not authenticated.
    """
    vacations = VacationDAO().get_all_vacations()
    countries = CountryDAO().get_all_countries()
    is_admin = session.get("role_id") == 2
    liked_vacations = LikeDAO().get_liked_vacation_ids_by_user(
        session["user_id"])

    return render_template("index.html", vacations=vacations, countries=countries, is_admin=is_admin, liked_vacations=liked_vacations)


@bp.route("/add-vacation", methods=["GET", "POST"])
@admin_required
def add_vacation():
    """
    Handles adding a vacation with validation and image upload.
    Access restricted to admin users.
    """
    countries = CountryDAO().get_all_countries()
    countries.sort(key=lambda c: c.country_name)

    if request.method == "POST":
        destination_id = request.form.get("destination_id")
        date_range = request.form.get("dateRangeInput")
        price_raw = request.form.get("price")
        vacation_info = request.form.get("vacation_info")
        file = request.files.get("image")
        
        form_data = {
            "destination": request.form.get("destination"),
            "destination_id": destination_id,
            "date_range": date_range,
            "price": price_raw,
            "vacation_info": vacation_info
        }

        if not all_fields_filled(destination_id, date_range, price_raw, vacation_info, file):
            flash("יש למלא את כל השדות", "error")
            return render_template("add-vacation.html", countries=countries, form_data=form_data)

        try:
            country_id = int(destination_id)
            price = int(''.join(filter(str.isdigit, price_raw)))
            start_str, end_str = map(str.strip, date_range.split(" - "))
            start_date = datetime.strptime(start_str, "%d/%m/%Y").date()
            end_date = datetime.strptime(end_str, "%d/%m/%Y").date()
            today = datetime.today().date()

        except Exception:
            flash("פורמט נתונים שגוי", "error")
            return render_template("add-vacation.html", countries=countries, form_data=form_data)

        if price <= 0 or price > 10_000:
            flash("יש להזין מחיר בין 1₪-10,000₪", "error")
            return render_template("add-vacation.html", countries=countries, form_data=form_data)

        if end_date < start_date:
            flash("תאריך סיום לא יכול להיות לפני תאריך התחלה", "error")
            return render_template("add-vacation.html", countries=countries, form_data=form_data)

        if start_date < today or end_date < today:
            flash("לא ניתן לבחור תאריכים שכבר עברו", "error")
            return render_template("add-vacation.html", countries=countries, form_data=form_data)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        try:
            VacationService().add_vacation(
                country_id, vacation_info, start_date, end_date, price, filename
            )
            flash("החופשה נוספה בהצלחה", "success")
            return redirect(url_for("vacations.add_vacation"))

        except Exception:
            flash("שגיאה בהוספת חופשה", "error")
            return render_template("add-vacation.html", countries=countries, form_data=form_data)

    # GET
    return render_template("add-vacation.html", countries=countries)


@bp.route("/edit-vacation/<int:vacation_id>", methods=["GET", "POST"])
@admin_required
def edit_vacation(vacation_id):
    vacation = VacationDAO().get_vacation_by_id(vacation_id)
    if not vacation:
        abort(404)

    countries = CountryDAO().get_all_countries()
    countries.sort(key=lambda c: c.country_name)

    if request.method == "POST":
        form_data = {
            "destination": request.form.get("destination"),
            "destination_id": request.form.get("destination_id"),
            "date_range": request.form.get("dateRangeInput"),
            "price": request.form.get("price"),
            "vacation_info": request.form.get("vacation_info"),
            "photo_file_path": vacation.photo_file_path
        }
        file = request.files.get("image")

        destination_id = form_data["destination_id"]
        date_range = form_data["date_range"]
        price_raw = form_data["price"]
        vacation_info = form_data["vacation_info"]

        if not all([destination_id, date_range, price_raw, vacation_info]):
            flash("יש למלא את כל השדות", "error")
            return render_template(
                "edit-vacation.html", vacation=vacation, countries=countries, form_data=form_data
            )

        try:
            country_id = int(destination_id)
            price = int(''.join(filter(str.isdigit, price_raw)))
            start_str, end_str = map(str.strip, date_range.split(" - "))
            start_date = datetime.strptime(start_str, "%d/%m/%Y").date()
            end_date = datetime.strptime(end_str, "%d/%m/%Y").date()
            
        except Exception:
            flash("פורמט נתונים שגוי", "error")
            return render_template(
                "edit-vacation.html", vacation=vacation, countries=countries, form_data=form_data
            )

        if price <= 0 or price > 10_000:
            flash("יש להזין מחיר בין 1₪ ל-10,000₪", "error")
            return render_template(
                "edit-vacation.html", vacation=vacation, countries=countries, form_data=form_data
            )

        if end_date < start_date:
            flash("תאריך הסיום לא יכול להיות מוקדם מתאריך ההתחלה", "error")
            return render_template(
                "edit-vacation.html", vacation=vacation, countries=countries, form_data=form_data
            )

        filename = vacation.photo_file_path
        if file and file.filename:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        try:
            VacationService().update_vacation(
                vacation_id, country_id, vacation_info,
                start_date, end_date, price, filename
            )
            flash("החופשה עודכנה בהצלחה", "success")
            return redirect(url_for("vacations.home_page"))
        except Exception:
            abort(500)

    # GET
    form_data = {
        "destination": vacation.country_name,
        "destination_id": vacation.country_id,
        "date_range": f"{vacation.vacation_start_date.strftime('%d/%m/%Y')} - {vacation.vacation_end_date.strftime('%d/%m/%Y')}",
        "price": vacation.price,
        "vacation_info": vacation.vacation_info,
        "photo_file_path": vacation.photo_file_path
    }

    return render_template(
        "edit-vacation.html",
        vacation=vacation,
        countries=countries,
        form_data=form_data
    )


@bp.route("/delete-vacation/<int:vacation_id>", methods=["POST"])
@admin_required
def delete_vacation(vacation_id):
    """
    Deletes a vacation by ID and returns JSON response.
    Access restricted to admin users.
    """
    vacation = VacationDAO().get_vacation_by_id(vacation_id)
    if not vacation:
        return jsonify({"success": False, "error": "Vacation not found"}), 404

    try:
        VacationService().delete_vacation(vacation_id)
        return jsonify({"success": True}), 200

    except Exception:
        return jsonify({"success": False, "error": "שגיאה במחיקה"}), 500

    
@bp.route("/like", methods=["POST"])
@login_required
def toggle_like():
    data = request.get_json()
    vacation_id = data.get("vacation_id")
    user_id = session.get("user_id")

    if not vacation_id or not user_id:
        return jsonify({"error": "Missing data"}), 400

    try:
        vacation_id = int(vacation_id)
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400

    if LikeDAO().get_like_by_user_and_vacation(user_id, vacation_id):
        UserService().remove_like(user_id, vacation_id)
        action = "removed"
    else:
        UserService().add_like(user_id, vacation_id)
        action = "added"

    updated_vacation = next(
        (v for v in VacationService().get_vacations() if v.vacation_id == vacation_id),
        None
    )

    if not updated_vacation:
        return jsonify({"error": "Vacation not found after update"}), 404

    return jsonify({
        "likes_count": updated_vacation.likes_count,
        "message": f"Like {action} successfully"
    }), 200

#
