from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired

class InboundMailAppointmentForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_tin = StringField('Company TIN', validators=[DataRequired()])
    company_address = TextAreaField('Company Address', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    letter_title = StringField('Letter Title')
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    office = SelectField('Office', choices=[('Large Tax Office (Oil & Gas) Services', 'Large Tax Office (Oil & Gas) Services')], validators=[DataRequired()])
    
    # Existing fields
    mail_letter = BooleanField('Mail/Letter')
    vat = BooleanField('VAT')
    wht = BooleanField('WHT')
    annual_return = BooleanField('Annual Return')
    
    # New fields for VAT
    vat_amount = StringField('VAT Amount', validators=[DataRequired()], default='0')
    vat_bank = StringField('Bank for VAT', validators=[DataRequired()])
    vat_period_covered = StringField('VAT Period Covered', validators=[DataRequired()])

    # New fields for WHT
    wht_amount = StringField('WHT Amount', validators=[DataRequired()], default='0')
    wht_bank = StringField('Bank for WHT', validators=[DataRequired()])
    wht_period_covered = StringField('WHT Period Covered', validators=[DataRequired()])

    # New field for Annual Returns
    tax_period = StringField('Tax Period', validators=[DataRequired()])

    submit = SubmitField('Submit')
