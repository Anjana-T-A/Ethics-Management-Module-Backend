from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from users.models import Supervisor

class EthicalApprovalStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    UNDER_REVIEW = 'Under Review', 'Under Review'
    APPROVED = 'Approved', 'Approved'
    MAJOR_CLARIFICATIONS = 'Major Clarifications', 'Major Clarifications'
    MINOR_CLARIFICATIONS = 'Minor Clarifications', 'Minor Clarifications'
    REJECTED = 'Rejected', 'Rejected'

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

    # JSON Fields
    human_participants = models.JSONField(default=dict)
    subject_matter = models.JSONField(default=dict)

    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)

    approval_status = models.CharField(
        max_length=20,
        choices=EthicalApprovalStatus.choices,
        default=EthicalApprovalStatus.PENDING
    )

    def clean(self):
        """Validate JSON Fields before saving"""
        expected_human_keys = {"vulnerable_persons", "under_18", "patients", "staff"}
        expected_subject_keys = {"sensitive_issues", "illegal_activities", "self_respect_risk"}

        # Validate human_participants
        if not isinstance(self.human_participants, dict):
            raise ValidationError({"human_participants": "Invalid format. Expected a JSON object."})
        if set(self.human_participants.keys()) != expected_human_keys:
            raise ValidationError({"human_participants": f"Missing or extra fields. Expected {expected_human_keys}."})
        if not all(isinstance(value, bool) for value in self.human_participants.values()):
            raise ValidationError({"human_participants": "All values must be boolean (true/false)."})

        # Validate subject_matter
        if not isinstance(self.subject_matter, dict):
            raise ValidationError({"subject_matter": "Invalid format. Expected a JSON object."})
        if set(self.subject_matter.keys()) != expected_subject_keys:
            raise ValidationError({"subject_matter": f"Missing or extra fields. Expected {expected_subject_keys}."})
        if not all(isinstance(value, bool) for value in self.subject_matter.values()):
            raise ValidationError({"subject_matter": "All values must be boolean (true/false)."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

        from .tasks import notify_reviewer
        notify_reviewer.apply_async(args=[self.id])
