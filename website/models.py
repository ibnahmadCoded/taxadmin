from . import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .admin_metrics import CustomAdminIndexView  # Import the custom admin view

# Define the Appointment model
class InboundMails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    letter_title = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    receipt_date = db.Column(db.Date)  
    office = db.Column(db.String(50), nullable=False, default='Large Tax Office (Oil & Gas) Services')
    recipient = db.Column(db.String(100), nullable=True)  
    received = db.Column(db.Boolean, default=False)  

    def __repr__(self):
        return f"<Appointment {self.company_name}>"

class InboundMailsAdmin(ModelView):
    form_columns = [
        "company_name",
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

def setup_admin(app):
    admin = Admin(app, name="TaxAdmin Dashboard", template_mode="bootstrap3", index_view=CustomAdminIndexView())
    admin.add_view(InboundMailsAdmin(db.session))
