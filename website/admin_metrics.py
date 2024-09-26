from flask_admin import AdminIndexView
from flask_admin.base import expose
from datetime import datetime, timedelta
from . import db

class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Import the model here to avoid circular imports
        from .models import InboundMails, VAT, WHT, OutgoingFiles, IncomingFiles, NewFileOpening, DocumentDispatch, AnnualReturns, TCCApplications

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

        # Consolidate pending counts for today
        pending_today = (
            InboundMails.query.filter(
                InboundMails.appointment_date == today.date(),
                InboundMails.received == False  # noqa: E712
            ).count() +
            VAT.query.filter(
                VAT.appointment_date== today.date(),
                VAT.received == False  # noqa: E712
            ).count() +
            WHT.query.filter(
                WHT.appointment_date== today.date(),
                WHT.received == False  # noqa: E712
            ).count() +
            AnnualReturns.query.filter(
                AnnualReturns.appointment_date== today.date(),
                AnnualReturns.received == False  # noqa: E712
            ).count()
        )

        # Consolidate pending counts for this week
        pending_this_week = (
            InboundMails.query.filter(
                InboundMails.appointment_date >= start_of_week.date(),
                InboundMails.received == False  # noqa: E712
            ).count() +
            VAT.query.filter(
                VAT.appointment_date>= start_of_week.date(),
                VAT.received == False  # noqa: E712
            ).count() +
            WHT.query.filter(
                WHT.appointment_date>= start_of_week.date(),
                WHT.received == False  # noqa: E712
            ).count() +
            AnnualReturns.query.filter(
                AnnualReturns.appointment_date>= start_of_week.date(),
                AnnualReturns.received == False  # noqa: E712
            ).count()
        )

        # Consolidate pending counts for this month
        pending_this_month = (
            InboundMails.query.filter(
                InboundMails.appointment_date >= start_of_month.date(),
                InboundMails.received == False  # noqa: E712
            ).count() +
            VAT.query.filter(
                VAT.appointment_date>= start_of_month.date(),
                VAT.received == False  # noqa: E712
            ).count() +
            WHT.query.filter(
                WHT.appointment_date>= start_of_month.date(),
                WHT.received == False  # noqa: E712
            ).count() +
            AnnualReturns.query.filter(
                AnnualReturns.appointment_date>= start_of_month.date(),
                AnnualReturns.received == False  # noqa: E712
            ).count()
        )

        # Consolidate pending counts for this year
        pending_this_year = (
            InboundMails.query.filter(
                InboundMails.appointment_date >= start_of_year.date(),
                InboundMails.received == False  # noqa: E712
            ).count() +
            VAT.query.filter(
                VAT.appointment_date>= start_of_year.date(),
                VAT.received == False  # noqa: E712
            ).count() +
            WHT.query.filter(
                WHT.appointment_date>= start_of_year.date(),
                WHT.received == False  # noqa: E712
            ).count() +
            AnnualReturns.query.filter(
                AnnualReturns.appointment_date>= start_of_year.date(),
                AnnualReturns.received == False  # noqa: E712
            ).count()
        )     
        
        # VAT metrics
        vat_totals_ngn_month = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_month.date(),
            VAT.currency == 'NGN',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_usd_month = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_month.date(),
            VAT.currency == 'USD',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_eur_month = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_month.date(),
            VAT.currency == 'EUR',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_gbp_month = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_month.date(),
            VAT.currency == 'GBP',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_ngn_year = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_year.date(),
            VAT.currency == 'NGN',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_usd_year = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_year.date(),
            VAT.currency == 'USD',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_eur_year = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_year.date(),
            VAT.currency == 'EUR',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        vat_totals_gbp_year = db.session.query(db.func.sum(VAT.amount)).filter(
            VAT.receipt_date>= start_of_year.date(),
            VAT.currency == 'GBP',
            VAT.received == True # noqa: E712
        ).scalar() or 0

        # WHT metrics
        wht_totals_ngn_month = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_month.date(),
            WHT.currency == 'NGN',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_usd_month = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_month.date(),
            WHT.currency == 'USD',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_eur_month = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_month.date(),
            WHT.currency == 'EUR',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_gbp_month = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_month.date(),
            WHT.currency == 'GBP',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_ngn_year = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_year.date(),
            WHT.currency == 'NGN',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_usd_year = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_year.date(),
            WHT.currency == 'USD',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_eur_year = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_year.date(),
            WHT.currency == 'EUR',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        wht_totals_gbp_year = db.session.query(db.func.sum(WHT.amount)).filter(
            WHT.receipt_date>= start_of_year.date(),
            WHT.currency == 'GBP',
            WHT.received == True # noqa: E712
        ).scalar() or 0

        # VAT Counts
        vat_today = VAT.query.filter(
            VAT.receipt_date== today.date(),
            VAT.received == True  # noqa: E712
        ).count()

        vat_this_week = VAT.query.filter(
            VAT.receipt_date>= start_of_week.date(),
            VAT.received == True  # noqa: E712
        ).count()

        vat_this_month = VAT.query.filter(
            VAT.receipt_date>= start_of_month.date(),
            VAT.received == True  # noqa: E712
        ).count()

        vat_this_year = VAT.query.filter(
            VAT.receipt_date>= start_of_year.date(),
            VAT.received == True  # noqa: E712
        ).count()

        # WHT Counts
        wht_today = WHT.query.filter(
            WHT.receipt_date== today.date(),
            WHT.received == True  # noqa: E712
        ).count()

        wht_this_week = WHT.query.filter(
            WHT.receipt_date>= start_of_week.date(),
            WHT.received == True  # noqa: E712
        ).count()

        wht_this_month = WHT.query.filter(
            WHT.receipt_date>= start_of_month.date(),
            WHT.received == True  # noqa: E712
        ).count()

        wht_this_year = WHT.query.filter(
            WHT.receipt_date>= start_of_year.date(),
            WHT.received == True  # noqa: E712
        ).count()

        # Outgoing Files Counts
        outgoing_files_today = OutgoingFiles.query.filter(
            OutgoingFiles.date == today.date()
        ).count()

        outgoing_files_this_week = OutgoingFiles.query.filter(
            OutgoingFiles.date >= start_of_week.date()
        ).count()

        outgoing_files_this_month = OutgoingFiles.query.filter(
            OutgoingFiles.date >= start_of_month.date()
        ).count()

        outgoing_files_this_year = OutgoingFiles.query.filter(
            OutgoingFiles.date >= start_of_year.date()
        ).count()

        # Incoming Files Counts
        incoming_files_today = IncomingFiles.query.filter(
            IncomingFiles.date == today.date()
        ).count()

        incoming_files_this_week = IncomingFiles.query.filter(
            IncomingFiles.date >= start_of_week.date()
        ).count()

        incoming_files_this_month = IncomingFiles.query.filter(
            IncomingFiles.date >= start_of_month.date()
        ).count()

        incoming_files_this_year = IncomingFiles.query.filter(
            IncomingFiles.date >= start_of_year.date()
        ).count()

        # New File Openings Counts
        new_file_openings_today = NewFileOpening.query.filter(
            NewFileOpening.date == today.date()
        ).count()

        new_file_openings_this_week = NewFileOpening.query.filter(
            NewFileOpening.date >= start_of_week.date()
        ).count()

        new_file_openings_this_month = NewFileOpening.query.filter(
            NewFileOpening.date >= start_of_month.date()
        ).count()

        new_file_openings_this_year = NewFileOpening.query.filter(
            NewFileOpening.date >= start_of_year.date()
        ).count()

        # Document Dispatch Counts
        document_dispatch_today = DocumentDispatch.query.filter(
            DocumentDispatch.date_of_dispatch == today.date()
        ).count()

        document_dispatch_this_week = DocumentDispatch.query.filter(
            DocumentDispatch.date_of_dispatch >= start_of_week.date()
        ).count()

        document_dispatch_this_month = DocumentDispatch.query.filter(
            DocumentDispatch.date_of_dispatch >= start_of_month.date()
        ).count()

        document_dispatch_this_year = DocumentDispatch.query.filter(
            DocumentDispatch.date_of_dispatch >= start_of_year.date()
        ).count()

        # Annual Returns Counts
        annual_returns_today = AnnualReturns.query.filter(
            AnnualReturns.receipt_date== today.date(),
            AnnualReturns.received == True  # noqa: E712
        ).count()

        annual_returns_this_week = AnnualReturns.query.filter(
            AnnualReturns.receipt_date>= start_of_week.date(),
            AnnualReturns.received == True  # noqa: E712
        ).count()

        annual_returns_this_month = AnnualReturns.query.filter(
            AnnualReturns.receipt_date>= start_of_month.date(),
            AnnualReturns.received == True  # noqa: E712
        ).count()

        annual_returns_this_year = AnnualReturns.query.filter(
            AnnualReturns.receipt_date>= start_of_year.date(),
            AnnualReturns.received == True  # noqa: E712
        ).count()

        # TCC Applications Counts
        tcc_applications_today = TCCApplications.query.filter(
            TCCApplications.date_tcc_issued == today.date()
        ).count()

        tcc_applications_this_week = TCCApplications.query.filter(
            TCCApplications.date_tcc_issued >= start_of_week.date()
        ).count()

        tcc_applications_this_month = TCCApplications.query.filter(
            TCCApplications.date_tcc_issued >= start_of_month.date()
        ).count()

        tcc_applications_this_year = TCCApplications.query.filter(
            TCCApplications.date_tcc_issued >= start_of_year.date()
        ).count()


        return self.render('metrics.html',
                           mails_today=mails_today,
                           mails_this_week=mails_this_week,
                           mails_this_month=mails_this_month,
                           mails_this_year=mails_this_year,

                           pending_today=pending_today,
                           pending_this_week=pending_this_week,
                           pending_this_month=pending_this_month,
                           pending_this_year=pending_this_year,
                           
                           vat_totals_ngn_month=vat_totals_ngn_month,
                           vat_totals_ngn_year=vat_totals_ngn_year,
                           vat_totals_usd_month=vat_totals_usd_month,
                           vat_totals_usd_year=vat_totals_usd_year,
                           vat_totals_eur_month=vat_totals_eur_month,
                           vat_totals_eur_year=vat_totals_eur_year,
                           vat_totals_gbp_month=vat_totals_gbp_month,
                           vat_totals_gbp_year=vat_totals_gbp_year,
                           
                           wht_totals_ngn_month=wht_totals_ngn_month,
                           wht_totals_ngn_year=wht_totals_ngn_year,
                           wht_totals_usd_month=wht_totals_usd_month,
                           wht_totals_usd_year=wht_totals_usd_year,
                           wht_totals_eur_month=wht_totals_eur_month,
                           wht_totals_eur_year=wht_totals_eur_year,
                           wht_totals_gbp_month=wht_totals_gbp_month,
                           wht_totals_gbp_year=wht_totals_gbp_year,
                           
                           vat_today=vat_today,
                           vat_this_week=vat_this_week,
                           vat_this_month=vat_this_month,
                           vat_this_year=vat_this_year,
                           
                           wht_today=wht_today,
                           wht_this_week=wht_this_week,
                           wht_this_month=wht_this_month,
                           wht_this_year=wht_this_year,
                           
                           outgoing_files_today=outgoing_files_today,
                           outgoing_files_this_week=outgoing_files_this_week,
                           outgoing_files_this_month=outgoing_files_this_month,
                           outgoing_files_this_year=outgoing_files_this_year,
                           
                           incoming_files_today=incoming_files_today,
                           incoming_files_this_week=incoming_files_this_week,
                           incoming_files_this_month=incoming_files_this_month,
                           incoming_files_this_year=incoming_files_this_year,
                           
                           new_file_openings_today=new_file_openings_today,
                           new_file_openings_this_week=new_file_openings_this_week,
                           new_file_openings_this_month=new_file_openings_this_month,
                           new_file_openings_this_year=new_file_openings_this_year,
                           
                           document_dispatch_today=document_dispatch_today,
                           document_dispatch_this_week=document_dispatch_this_week,
                           document_dispatch_this_month=document_dispatch_this_month,
                           document_dispatch_this_year=document_dispatch_this_year,
                           
                           annual_returns_today=annual_returns_today,
                           annual_returns_this_week=annual_returns_this_week,
                           annual_returns_this_month=annual_returns_this_month,
                           annual_returns_this_year=annual_returns_this_year,
                           
                           tcc_applications_today=tcc_applications_today,
                           tcc_applications_this_week=tcc_applications_this_week,
                           tcc_applications_this_month=tcc_applications_this_month,
                           tcc_applications_this_year=tcc_applications_this_year,)
