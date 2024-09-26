from flask_admin import Admin
from flask_admin.menu import MenuLink
from wtforms import PasswordField
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from .models import db, InboundMails, VAT, WHT, OutgoingFiles, IncomingFiles, NewFileOpening, DocumentDispatch, AnnualReturns, TCCApplications, User
from .admin_metrics import CustomAdminIndexView

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class SecureCustomAdminIndexView(CustomAdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class UserAdmin(SecureModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    column_auto_select_related = True

    # Override the scaffold_form method to include a password field
    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        # Add a password field
        form_class.password = PasswordField('Password')

        return form_class

    # Override the is_accessible method to allow all authenticated users
    def is_accessible(self):
        return current_user.is_authenticated

    # Allow users to only edit their own profile unless they are a superuser
    def get_query(self):
        if current_user.is_superuser:
            return super(UserAdmin, self).get_query()
        else:
            # Regular users can only query their own profile
            return super(UserAdmin, self).get_query().filter(User.id == current_user.id)

    def get_count_query(self):
        if current_user.is_superuser:
            return super(UserAdmin, self).get_count_query()
        else:
            # Regular users can only see their own count
            return super(UserAdmin, self).get_count_query().filter(User.id == current_user.id)

    # Override on_model_change to set the password using set_password method
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            # Use the set_password method from the User model to hash and store the password
            model.set_password(form.password.data)
        super(UserAdmin, self).on_model_change(form, model, is_created)

    # Prevent regular users from deleting their profile or others
    def delete_model(self, model):
        if current_user.is_superuser:
            super(UserAdmin, self).delete_model(model)
        else:
            flash("You are not allowed to delete your profile.")
    
    # Prevent non-superusers from creating new profiles
    def create_model(self, form):
        if current_user.is_superuser:
            super(UserAdmin, self).create_model(form)
        else:
            flash("You are not allowed to create new profiles.")


class InboundMailsAdmin(SecureModelView):
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
class VATAdmin(SecureModelView):
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
class WHTAdmin(SecureModelView):
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
class OutgoingFilesAdmin(SecureModelView):
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
class IncomingFilesAdmin(SecureModelView):
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
class NewFileOpeningAdmin(SecureModelView):
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
class DocumentDispatchAdmin(SecureModelView):
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
class AnnualReturnsAdmin(SecureModelView):
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
class TCCApplicationsAdmin(SecureModelView):
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
    admin = Admin(app, name="TaxAdmin Dashboard", template_mode="bootstrap3", index_view=SecureCustomAdminIndexView(db.session))
    
    # Add each admin view for all models
    admin.add_view(OutgoingFilesAdmin(db.session, category='Files'))
    admin.add_view(IncomingFilesAdmin(db.session, category='Files'))
    admin.add_view(NewFileOpeningAdmin(db.session, category='Files'))
    admin.add_view(DocumentDispatchAdmin(db.session, category='Files'))

    admin.add_view(TCCApplicationsAdmin(db.session))

    admin.add_view(InboundMailsAdmin(db.session, category='External Correspondence'))  # Existing
    admin.add_view(VATAdmin(db.session, category='External Correspondence'))
    admin.add_view(WHTAdmin(db.session, category='External Correspondence'))
    admin.add_view(AnnualReturnsAdmin(db.session, category='External Correspondence'))
    

    admin.add_view(UserAdmin(User, db.session, name='Users', category='Settings'))
    admin.add_link(MenuLink(name='Logout', category='Settings', url="/logout"))

    # Additional customization for CSS (if needed)
    # You can also consider using a separate CSS file if your customization grows
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'  # You can customize the Bootstrap theme here if needed
