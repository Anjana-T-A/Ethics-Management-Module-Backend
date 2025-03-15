from celery import shared_task
from .models import EthicsForm
from celery import shared_task
from django.core.mail import send_mail
from ethics.models import EthicsForm
from users.models import Supervisor, Reviewer

@shared_task
def notify_reviewer(ethics_form_id):
    """
    Fetches the ethics form details and formats them as a structured response
    for the frontend instead of sending an email.
    """
    # Get the EthicsForm instance
    ethics_form = EthicsForm.objects.get(id=ethics_form_id)

    reviewer = Reviewer.objects.filter(department=ethics_form.supervisor.department).first()

    if reviewer:
        # Structure the notification data
        notification_data = {
            "title": "New Ethics Application Submitted",
            "ethics_form_id": ethics_form.id,
            "application_title": ethics_form.application_title,
            "applicant_name": ethics_form.applicant_name,
            "supervisor_name": ethics_form.supervisor_name,
            "status": ethics_form.approval_status,
            "start_date": ethics_form.start_date.strftime("%Y-%m-%d"),
            "end_date": ethics_form.end_date.strftime("%Y-%m-%d"),
            "declaration_date": ethics_form.declaration_date.strftime("%Y-%m-%d"),
            "reviewer": {
                "name": reviewer.user.get_full_name(),
                "email": reviewer.user.email,
            },
            "message": f"An ethics application titled '{ethics_form.application_title}' has been submitted by {ethics_form.applicant_name} for review."
        }

        return notification_data
    
    return {"error": "No suitable reviewer found for this department."}
