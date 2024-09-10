from flask import Blueprint, render_template, redirect, url_for
from .models import Appointment
from .forms import AppointmentForm
from . import db

views = Blueprint("views", __name__)

# Main route to show the appointment form
@views.route("/", methods=["GET", "POST"])
def index():
    form = AppointmentForm()
    if form.validate_on_submit():
        # Create a new appointment object
        new_appointment = Appointment(
            name=form.name.data,
            company_name=form.company_name.data,
            letter_title=form.letter_title.data,
            appointment_date=form.appointment_date.data,
            recipient="Admin Name"  # Set recipient as admin name, dynamic if needed
        )
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for("views.index"))
    
    return render_template("index.html", form=form)
