from . import db
from flask_admin import Admin
from wtforms import ValidationError  
from flask_admin.contrib.sqla import ModelView


# Define the Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    letter_title = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    receipt_date = db.Column(db.Date)  
    office = db.Column(db.String(50), nullable=False, default='Large Tax Office (Oil & Gas) Services')
    recipient = db.Column(db.String(100), nullable=True)  
    received = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f"<Appointment {self.name} - {self.company_name}>"

# Set up the admin interface for appointments
class AppointmentAdmin(ModelView):
    form_columns = [
        "name",
        "company_name",
        "letter_title",
        "appointment_date",
        "receipt_date", 
        "office",        
        "recipient",     
        "received",      
    ]

    # Prevent editing if the appointment is marked as received
    def on_model_change(self, form, model, is_created):
        if model.received:
            raise ValidationError("This entry has been marked as received and cannot be edited.")

    column_editable_list = ['received']  # Allow editing the 'received' field

# Function to set up the admin
def setup_admin(app):
    admin = Admin(app, name="Admin Dashboard", template_mode="bootstrap3")
    admin.add_view(AppointmentAdmin(Appointment, db.session))
