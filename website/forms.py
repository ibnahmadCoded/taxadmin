from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired

# Create the Appointment form
class AppointmentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    company_name = StringField(
        "Company Name (not Consulting company if applicable)", validators=[DataRequired()]
    )
    letter_title = StringField("Letter Title", validators=[DataRequired()])
    appointment_date = DateField(
        "Appointment Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    office = SelectField(
        "Office", choices=[('Large Tax Office (Oil & Gas) Services', 'Large Tax Office (Oil & Gas) Services'), 
                           ('Small Tax Office', 'Small Tax Office')], default="Large Tax Office (Oil & Gas) Services"
    )
