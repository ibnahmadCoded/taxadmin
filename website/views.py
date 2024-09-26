from flask import Blueprint, render_template, redirect, url_for, flash
from .models import InboundMails, VAT, WHT, AnnualReturns
from .forms import InboundMailAppointmentForm
from . import db

views = Blueprint("views", __name__)

# Main route to show the appointment form
@views.route("/", methods=["GET", "POST"])
def index():
    form = InboundMailAppointmentForm()
    
    if form.validate_on_submit():
        try:
            # Check which checkboxes are selected and handle accordingly
            if form.mail_letter.data:
                # Create a new InboundMails object if the mail/letter checkbox is checked
                new_appointment = InboundMails(
                    company_name=form.company_name.data,
                    company_tin=form.company_tin.data,
                    company_address=form.company_address.data,
                    contact_number=form.contact_number.data,
                    letter_title=form.letter_title.data,
                    appointment_date=form.appointment_date.data,
                    recipient="None"  # Set recipient as admin name
                )
                db.session.add(new_appointment)

            if form.vat.data:
                # Create a new VAT object if the VAT checkbox is checked
                new_vat = VAT(
                    tin=form.company_tin.data,
                    company_name=form.company_name.data,
                    company_address=form.company_address.data,
                    contact_number=form.contact_number.data,
                    amount=form.vat_amount.data,  # Use DecimalField value for VAT amount
                    currency=form.vat_currency.data,
                    bank=form.vat_bank.data,  # Use form data for VAT bank
                    period_covered=form.vat_period_covered.data,  # Use form data for VAT period
                    appointment_date=form.appointment_date.data  # Set date to the appointment date
                )
                db.session.add(new_vat)

            if form.wht.data:
                # Create a new WHT object if the WHT checkbox is checked
                new_wht = WHT(
                    tin=form.company_tin.data,
                    company_name=form.company_name.data,
                    company_address=form.company_address.data,
                    contact_number=form.contact_number.data,
                    amount=form.wht_amount.data,  # Use form data for WHT amount
                    currency=form.wht_currency.data,
                    bank=form.wht_bank.data,  # Use form data for WHT bank
                    period_covered=form.wht_period_covered.data,  # Use form data for WHT period
                    appointment_date=form.appointment_date.data  # Set date to the appointment date
                )
                db.session.add(new_wht)

            if form.annual_return.data:
                # Create a new AnnualReturns object if the Annual Returns checkbox is checked
                new_annual_return = AnnualReturns(
                    appointment_date=form.appointment_date.data,  # Set return received date
                    tin=form.company_tin.data,
                    company_name=form.company_name.data,
                    address=form.company_address.data,
                    tax_period=form.tax_period.data  # Use form data for tax period
                )
                db.session.add(new_annual_return)

            # Commit all changes to the database
            db.session.commit()
            flash("Appointment successfully created!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for("views.index"))
    
    return render_template("index.html", form=form)
