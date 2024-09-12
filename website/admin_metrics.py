from flask_admin import AdminIndexView
from flask_admin.base import expose
from datetime import datetime, timedelta
from . import db

class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Import the model here to avoid circular imports
        from .models import InboundMails

        # Define the date ranges
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        # Count the received mails per day, week, month, and year
        mails_today = InboundMails.query.filter(
            InboundMails.receipt_date == today.date(),
            InboundMails.received == True  # noqa: E712
        ).count()

        mails_this_week = InboundMails.query.filter(
            InboundMails.receipt_date >= start_of_week.date(),
            InboundMails.received == True  # noqa: E712
        ).count()

        mails_this_month = InboundMails.query.filter(
            InboundMails.receipt_date >= start_of_month.date(),
            InboundMails.received == True  # noqa: E712
        ).count()

        mails_this_year = InboundMails.query.filter(
            InboundMails.receipt_date >= start_of_year.date(),
            InboundMails.received == True  # noqa: E712
        ).count()

        # Count received mails by recipient for this month
        recipient_counts_month = db.session.query(
            InboundMails.recipient, db.func.count(InboundMails.id)
        ).filter(
            InboundMails.receipt_date >= start_of_month.date(),
            InboundMails.received == True  # noqa: E712
        ).group_by(InboundMails.recipient).order_by(db.func.count(InboundMails.id).desc()).limit(5).all()

        # Count received mails by recipient for this year
        recipient_counts_year = db.session.query(
            InboundMails.recipient, db.func.count(InboundMails.id)
        ).filter(
            InboundMails.receipt_date >= start_of_year.date(),
            InboundMails.received == True  # noqa: E712
        ).group_by(InboundMails.recipient).order_by(db.func.count(InboundMails.id).desc()).limit(5).all()

        # Count pending appointments per day, week, month, and year
        pending_today = InboundMails.query.filter(
            InboundMails.appointment_date == today.date(),
            InboundMails.received == False  # noqa: E712
        ).count()

        pending_this_week = InboundMails.query.filter(
            InboundMails.appointment_date >= start_of_week.date(),
            InboundMails.received == False  # noqa: E712
        ).count()

        pending_this_month = InboundMails.query.filter(
            InboundMails.appointment_date >= start_of_month.date(),
            InboundMails.received == False  # noqa: E712
        ).count()

        pending_this_year = InboundMails.query.filter(
            InboundMails.appointment_date >= start_of_year.date(),
            InboundMails.received == False  # noqa: E712
        ).count()

        # Count mails per company for this month and get the top 5 companies
        company_counts_month = db.session.query(
            InboundMails.company_name, db.func.count(InboundMails.id)
        ).filter(
            InboundMails.receipt_date >= start_of_month.date(),
            InboundMails.received == True  # noqa: E712
        ).group_by(InboundMails.company_name).order_by(db.func.count(InboundMails.id).desc()).limit(5).all()

        # Count mails per company for this year and get the top 5 companies
        company_counts_year = db.session.query(
            InboundMails.company_name, db.func.count(InboundMails.id)
        ).filter(
            InboundMails.receipt_date >= start_of_year.date(),
            InboundMails.received == True  # noqa: E712
        ).group_by(InboundMails.company_name).order_by(db.func.count(InboundMails.id).desc()).limit(5).all()

        return self.render('metrics.html',
                           mails_today=mails_today,
                           mails_this_week=mails_this_week,
                           mails_this_month=mails_this_month,
                           mails_this_year=mails_this_year,
                           recipient_counts_month=recipient_counts_month,
                           recipient_counts_year=recipient_counts_year,
                           pending_today=pending_today,
                           pending_this_week=pending_this_week,
                           pending_this_month=pending_this_month,
                           pending_this_year=pending_this_year,
                           company_counts_month=company_counts_month,
                           company_counts_year=company_counts_year)
