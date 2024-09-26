from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class InboundMailAppointmentForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_tin = StringField('Company TIN', validators=[DataRequired()])
    company_address = TextAreaField('Company Address', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    letter_title = StringField('Letter Title', validators=[Optional()])
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    office = SelectField('Office', choices=[('Large Tax Office (Oil & Gas) Services', 'Large Tax Office (Oil & Gas) Services')], validators=[DataRequired()])
    
    # Appointment Reason Fields
    mail_letter = BooleanField('Mail/Letter')
    vat = BooleanField('VAT')
    wht = BooleanField('WHT')
    annual_return = BooleanField('Annual Return')
    
    # VAT Fields
    vat_amount = DecimalField('VAT Amount', validators=[Optional(), NumberRange(min=0)], places=2, default=0.00)
    vat_currency = SelectField('VAT Currency', choices=[('NGN', 'NGN'), ('USD', 'USD'), ('GBP', 'GBP'), ('EUR', 'EUR')], validators=[Optional()])
    vat_bank = StringField('Bank for VAT', validators=[Optional()])
    vat_period_covered = StringField('VAT Period Covered', validators=[Optional()])
    
    # WHT Fields
    wht_amount = DecimalField('WHT Amount', validators=[Optional(), NumberRange(min=0)], places=2, default=0.00)
    wht_currency = SelectField('WHT Currency', choices=[('NGN', 'NGN'), ('USD', 'USD'), ('GBP', 'GBP'), ('EUR', 'EUR')], validators=[Optional()])
    wht_bank = StringField('Bank for WHT', validators=[Optional()])
    wht_period_covered = StringField('WHT Period Covered', validators=[Optional()])
    
    # Annual Returns Fields
    tax_period = StringField('Tax Period', validators=[Optional()])
    
    submit = SubmitField('Submit')
