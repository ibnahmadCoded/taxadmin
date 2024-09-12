from flask import Blueprint, render_template, redirect, url_for, flash
from .models import InboundMails
from .forms import InboundMailAppointmentForm
from . import db

views = Blueprint("views", __name__)

# Main route to show the appointment form
@views.route("/", methods=["GET", "POST"])
def index():
    form = InboundMailAppointmentForm()
    if form.validate_on_submit():
        try:
            # Create a new appointment object
            new_appointment = InboundMails(
                company_name=form.company_name.data,
                letter_title=form.letter_title.data,
                appointment_date=form.appointment_date.data,
                recipient="Admin Name"  # Set recipient as admin name, dynamic if needed
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash("Appointment successfully created!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for("views.index"))
    
    return render_template("index.html", form=form)
