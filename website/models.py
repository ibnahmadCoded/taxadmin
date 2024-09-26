from . import db
from flask_admin import Admin
from sqlalchemy import Numeric
from flask_admin.contrib.sqla import ModelView
from .admin_metrics import CustomAdminIndexView  # Import the custom admin view

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



class InboundMailsAdmin(ModelView):
    form_columns = ["company_name",
        "company_tin",  
        "company_address",  
        "contact_number",  
        "letter_title",
        "appointment_date",
        "receipt_date", 
        "office",        
        "recipient",     
        "received",      
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(InboundMails, session, **kwargs)
        self.name = 'Inbound Mails'

# VAT Admin View
class VATAdmin(ModelView):
    form_columns = [
        "tin",
        "company_name",
        "company_address",
        "contact_number",
        "currency",
        "amount",
        "bank",
        "period_covered",
        "appointment_date", 
        "receipt_date",
        "received" 
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(VAT, session, **kwargs)
        self.name = 'Value Added Tax'

# WHT Admin View
class WHTAdmin(ModelView):
    form_columns = [
        "tin",
        "company_name",
        "company_address",
        "contact_number",
        "currency",
        "amount",
        "bank",
        "period_covered",
        "appointment_date", 
        "receipt_date",
        "received"
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(WHT, session, **kwargs)
        self.name = 'Witholding Tax'

# Outgoing Files Admin View
class OutgoingFilesAdmin(ModelView):
    form_columns = [
        "tin",
        "company_name",
        "office_transferred_to",
        "pnj",
        "assmt",
        "vat",
        "wht",
        "coll",
        "remark",
        "sent_by",
        "date",
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(OutgoingFiles, session, **kwargs)
        self.name = 'Outgoing Files'

# Incoming Files Admin View
class IncomingFilesAdmin(ModelView):
    form_columns = [
        "tin",
        "company_name",
        "office_transferred_from",
        "pnj",
        "assmt",
        "vat",
        "wht",
        "coll",
        "remark",
        "received_by",
        "date",
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(IncomingFiles, session, **kwargs)
        self.name = 'Incoming Files'

# New File Opening Admin View
class NewFileOpeningAdmin(ModelView):
    form_columns = [
        "tin",
        "company_name",
        "file_type",  # Renamed to 'file_type' for clarity
        "opened_by",
        "date",
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(NewFileOpening, session, **kwargs)
        self.name = 'New File Opening'

# Document Dispatch Admin View
class DocumentDispatchAdmin(ModelView):
    form_columns = [
        "company_name",
        "office_to_dispatch_to",
        "item",
        "date_of_dispatch",
        "date_of_acknowledgement",
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(DocumentDispatch, session, **kwargs)
        self.name = 'Document Dispatch'

# Annual Returns Admin View
class AnnualReturnsAdmin(ModelView):
    form_columns = [
        "tin",
        "company_name",
        "address",
        "tax_period",
        "appointment_date", 
        "receipt_date",
        "received"
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(AnnualReturns, session, **kwargs)
        self.name = 'Annual Returns'

# TCC Applications Admin View
class TCCApplicationsAdmin(ModelView):
    form_columns = [
        "date_application_received",
        "company_name",
        "address",
        "nature_of_business",
        "tin",
        "tcc_granted",
        "date_granted_rejected",
        "ground_for_rejection",
        "date_tcc_issued",
    ]

    # Set the name to be displayed in the admin interface
    def __init__(self, session, **kwargs):
        super().__init__(TCCApplications, session, **kwargs)
        self.name = 'TCC Application'

# Setup Flask-Admin and add all views
def setup_admin(app):
    admin = Admin(app, name="TaxAdmin Dashboard", template_mode="bootstrap3", index_view=CustomAdminIndexView())
    
    # Add each admin view for all models
    admin.add_view(InboundMailsAdmin(db.session))  # Existing
    admin.add_view(VATAdmin(db.session))
    admin.add_view(WHTAdmin(db.session))
    admin.add_view(OutgoingFilesAdmin(db.session))
    admin.add_view(IncomingFilesAdmin(db.session))
    admin.add_view(NewFileOpeningAdmin(db.session))
    admin.add_view(DocumentDispatchAdmin(db.session))
    admin.add_view(AnnualReturnsAdmin(db.session))
    admin.add_view(TCCApplicationsAdmin(db.session))

"""def setup_admin(app):
    admin = Admin(app, name="TaxAdmin Dashboard", template_mode="bootstrap3", index_view=CustomAdminIndexView())
    admin.add_view(InboundMailsAdmin(db.session))"""
