from . import db
from sqlalchemy import Numeric
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_superuser = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the Appointment model
class InboundMails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_tin = db.Column(db.String(100), nullable=False)  # New field for TIN
    company_address = db.Column(db.Text, nullable=False)  # New field for address
    contact_number = db.Column(db.String(20), nullable=False)
    letter_title = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    receipt_date = db.Column(db.Date)  
    office = db.Column(db.String(50), nullable=False, default='Large Tax Office (Oil & Gas) Services')
    recipient = db.Column(db.String(100), nullable=True)  
    received = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f"<Appointment {self.company_name}>"
    
class VAT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tin = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    company_address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(Numeric(precision=10, scale=2), nullable=False)  # Decimal field for amount with two decimal places
    currency = db.Column(db.String(10), nullable=False)  # New field for currency
    bank = db.Column(db.String(100), nullable=False)
    period_covered = db.Column(db.String(50), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    receipt_date = db.Column(db.Date)
    received = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f"<VAT {self.company_name}>"


class WHT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tin = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    company_address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(Numeric(precision=10, scale=2), nullable=False)  # Decimal field for amount with two decimal places
    currency = db.Column(db.String(10), nullable=False)  # New field for currency
    bank = db.Column(db.String(100), nullable=False)
    period_covered = db.Column(db.String(50), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    receipt_date = db.Column(db.Date)
    received = db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return f"<WHT {self.company_name}>"
    
class OutgoingFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tin = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    office_transferred_to = db.Column(db.String(100), nullable=False)
    pnj = db.Column(db.String(100), nullable=True)
    assmt = db.Column(db.String(100), nullable=True)
    vat = db.Column(db.String(100), nullable=True)
    wht = db.Column(db.String(100), nullable=True)
    coll = db.Column(db.String(100), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    sent_by = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<OutgoingFiles {self.company_name}>"

class IncomingFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tin = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    office_transferred_from = db.Column(db.String(100), nullable=False)
    pnj = db.Column(db.String(100), nullable=True)
    assmt = db.Column(db.String(100), nullable=True)
    vat = db.Column(db.String(100), nullable=True)
    wht = db.Column(db.String(100), nullable=True)
    coll = db.Column(db.String(100), nullable=True)
    remark = db.Column(db.Text, nullable=True)
    received_by = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<IncomingFiles {self.company_name}>"

class NewFileOpening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tin = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    file_type = db.Column(db.String(100), nullable=False)  # 'Type' renamed to avoid conflicts
    opened_by = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<NewFileOpening {self.company_name}>"

class DocumentDispatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    office_to_dispatch_to = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    date_of_dispatch = db.Column(db.Date, nullable=False)
    date_of_acknowledgement = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<DocumentDispatch {self.company_name}>"

class AnnualReturns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tin = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    tax_period = db.Column(db.String(50), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    receipt_date = db.Column(db.Date)
    received = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<AnnualReturns {self.company_name}>"

class TCCApplications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_application_received = db.Column(db.Date, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    nature_of_business = db.Column(db.String(100), nullable=False)
    tin = db.Column(db.String(100), nullable=False)
    tcc_granted = db.Column(db.Boolean, nullable=False)  # Yes/No
    date_granted_rejected = db.Column(db.Date, nullable=False)
    ground_for_rejection = db.Column(db.Text, nullable=True)
    date_tcc_issued = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<TCCApplications {self.company_name}>"