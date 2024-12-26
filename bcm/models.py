from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from main_app.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


# Choices for frequencies and statuses
FREQUENCY_CHOICES = [
    ('DAILY', 'Daily'),
    ('WEEKLY', 'Weekly'),
    ('MONTHLY', 'Monthly'),
    ('QUARTERLY', 'Quarterly'),
    ('ANNUALLY', 'Annually'),
]

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('IN_PROGRESS', 'In Progress'),
    ('COMPLETED', 'Completed'),
]

class BCMGovernance(models.Model):
    governance_id = models.AutoField(primary_key=True)
    bcm_policy_title = models.CharField(max_length=255)
    approver_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='approver_governance')
    roles_and_responsibilities = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    approval_date = models.DateField(blank=True, null=True)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    governance_owner = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='owner_governance')
    supporting_documents = models.FileField(upload_to='governance_documents/')
    review_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

class BusinessImpactAnalysis(models.Model):
    bia_id = models.AutoField(primary_key=True)
    business_function = models.CharField(max_length=255)
    impact_level = models.CharField(max_length=50)
    dependencies = models.TextField(blank=True, null=True)
    maximum_tolerable_downtime = models.IntegerField(blank=True, null=True)
    recovery_time_objective = models.IntegerField(blank=True, null=True)
    critical_resources = models.TextField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    impact_description = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    comments = models.TextField(blank=True, null=True)

class ContinuityRiskAssessment(models.Model):
    risk_assessment_id = models.AutoField(primary_key=True)
    risk_name = models.CharField(max_length=255)
    impact_likelihood = models.CharField(max_length=50)
    risk_severity = models.CharField(max_length=50)
    associated_bcp = models.TextField(blank=True, null=True)
    mitigation_plan = models.TextField(blank=True, null=True)
    risk_owner = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    assessment_date = models.DateField(blank=True, null=True)
    review_cycle = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    supporting_documents = models.FileField(upload_to='risk_documents/')
    comments = models.TextField(blank=True, null=True)

class ContinuityStrategy(models.Model):
    strategy_id = models.AutoField(primary_key=True)
    strategy_name = models.CharField(max_length=255)
    recovery_objective = models.TextField(blank=True, null=True)
    resources_required = models.TextField(blank=True, null=True)
    third_party_dependencies = models.TextField(blank=True, null=True)
    associated_business_functions = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    approval_date = models.DateField(blank=True, null=True)
    reviewer_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    comments = models.TextField(blank=True, null=True)

class BusinessContinuityPlan(models.Model):
    bcp_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=255)
    business_function = models.CharField(max_length=255)
    plan_owner = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    recovery_steps = models.TextField(blank=True, null=True)
    contact_list = models.TextField(blank=True, null=True)
    activation_criteria = models.TextField(blank=True, null=True)
    testing_schedule = models.TextField(blank=True, null=True)
    last_test_date = models.DateField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    comments = models.TextField(blank=True, null=True)

class ContinuityTesting(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_scenario = models.TextField(blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    participants = models.TextField(blank=True, null=True)
    test_results = models.TextField(blank=True, null=True)
    issues_identified = models.TextField(blank=True, null=True)
    improvement_plan = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    next_scheduled_test = models.DateField(blank=True, null=True)
    reviewed_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    comments = models.TextField(blank=True, null=True)

class IncidentActivationLog(models.Model):
    incident_id = models.AutoField(primary_key=True)
    incident_type = models.CharField(max_length=255)
    date_activated = models.DateField(blank=True, null=True)
    bcp_activated = models.BooleanField(blank=True, null=True)
    decision_maker = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    resources_mobilized = models.TextField(blank=True, null=True)
    status_updates = models.TextField(blank=True, null=True)
    closure_date = models.DateField(blank=True, null=True)
    lessons_learned = models.TextField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='incident_documents/')
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.incident_type

class CrisisCommunication(models.Model):
    communication_id = models.AutoField(primary_key=True)
    incident_id = models.ForeignKey(IncidentActivationLog, blank=True, null=True, on_delete=models.SET_NULL)
    recipient_groups = models.TextField(blank=True, null=True)
    message_template = models.TextField(blank=True, null=True)
    date_sent = models.DateField(blank=True, null=True)
    sent_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    acknowledgment_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    follow_up_required = models.BooleanField(blank=True, null=True)
    escalation_plan = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='communication_attachments/')

class BCMProgramReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=255)
    reviewer_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    review_date = models.DateField(blank=True, null=True)
    key_findings = models.TextField(blank=True, null=True)
    compliance_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    improvement_recommendations = models.TextField(blank=True, null=True)
    implementation_plan = models.TextField(blank=True, null=True)
    follow_up_actions = models.TextField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='review_documents/')
    comments = models.TextField(blank=True, null=True)

class BCMDocumentManagement(models.Model):
    document_id = models.AutoField(primary_key=True)
    document_title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    upload_date = models.DateField(blank=True, null=True)
    version = models.CharField(max_length=50)
    document_type = models.CharField(max_length=255)
    associated_plans = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    access_permissions = models.TextField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    file_link = models.URLField(blank=True, null=True)


