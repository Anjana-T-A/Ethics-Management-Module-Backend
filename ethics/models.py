from django.db import models
from django.contrib.auth.models import User
from users.models import Supervisor

class HumanParticipants(models.Model):
    vulnerable_persons = models.BooleanField(default=False)
    under_18 = models.BooleanField(default=False)
    patients = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    @classmethod
    def get_default(cls):
        obj, created = cls.objects.get_or_create(id=1)  # Ensure a default object exists
        return obj.pk

    def __str__(self):
        return f"Human Participants: {self.vulnerable_persons}, {self.under_18}, {self.patients}, {self.staff}"

class SubjectMatter(models.Model):
    sensitive_issues = models.BooleanField(default=False)
    illegal_activities = models.BooleanField(default=False)
    self_respect_risk = models.BooleanField(default=False)

    @classmethod
    def get_default(cls):
        obj, created = cls.objects.get_or_create(id=1)  # Ensure a default object exists
        return obj.pk

    def __str__(self):
        return f"Subject Matter: {self.sensitive_issues}, {self.illegal_activities}, {self.self_respect_risk}"

# Ethical Approval Status Choices
class EthicalApprovalStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    UNDER_REVIEW = 'Under Review', 'Under Review'
    APPROVED = 'Approved', 'Approved'
    MAJOR_CLARIFICATIONS = 'Major Clarifications', 'Major Clarifications'
    MINOR_CLARIFICATIONS = 'Minor Clarifications', 'Minor Clarifications'
    REJECTED = 'Rejected', 'Rejected'


# Ethics Form Model
class EthicsForm(models.Model):
    clarifications = models.TextField()
    application_title = models.CharField(max_length=255)
    application_number = models.CharField(max_length=255)
    supervisor_name = models.CharField(max_length=255)
    supervisor_email = models.EmailField()
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    project_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    declaration_date = models.DateField()

    # Foreign key references to human participants and subject matter
    human_participants = models.ForeignKey(
        HumanParticipants, on_delete=models.CASCADE, default=HumanParticipants.get_default
    )
    subject_matter = models.ForeignKey(
        SubjectMatter, on_delete=models.CASCADE, default=SubjectMatter.get_default
    )
    # Supervisor as a Foreign Key to Supervisor model
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)

    # Ethics decision and approval tracking fields
    approval_status = models.CharField(
        max_length=20,
        choices=EthicalApprovalStatus.choices,
        default=EthicalApprovalStatus.PENDING
    )

    def __str__(self):
        return f"Ethics Form: {self.application_title} - {self.application_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .tasks import notify_reviewer

        # After saving the EthicsForm, trigger the task to notify the reviewer
        notify_reviewer.apply_async(args=[self.id])