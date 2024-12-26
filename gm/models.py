from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from main_app.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


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

class GovernanceStructure(models.Model):
    structure_id = models.AutoField(primary_key=True)
    charter_name = models.CharField(max_length=255)
    approver_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    roles_and_responsibilities = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    approval_date = models.DateField(blank=True, null=True)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    stewardship_owner = models.ForeignKey(Staff, related_name='stewardship_owner', blank=True, null=True, on_delete=models.SET_NULL)
    supporting_documents = models.FileField(upload_to='governance_documents/')
    review_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

class LeadershipAccountability(models.Model):
    leadership_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255)
    responsibilities = models.TextField(blank=True, null=True)
    accountable_to = models.ForeignKey(Staff, related_name='accountable_to', blank=True, null=True, on_delete=models.SET_NULL)
    decision_authority = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    review_date = models.DateField(blank=True, null=True)
    role_owner = models.ForeignKey(Staff, related_name='role_owner', blank=True, null=True, on_delete=models.SET_NULL)
    key_metrics = models.TextField(blank=True, null=True)
    improvement_areas = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

class PurposeAndValues(models.Model):
    purpose_id = models.AutoField(primary_key=True)
    purpose_statement = models.TextField(blank=True, null=True)
    core_values = models.TextField(blank=True, null=True)
    ethical_principles = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(Staff, related_name='approved_by', blank=True, null=True, on_delete=models.SET_NULL)
    approval_date = models.DateField(blank=True, null=True)
    stakeholder_feedback = models.TextField(blank=True, null=True)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    stewardship_owner = models.ForeignKey(Staff, related_name='purpose_stewardship_owner', blank=True, null=True, on_delete=models.SET_NULL)
    supporting_documents = models.FileField(upload_to='purpose_documents/')
    comments = models.TextField(blank=True, null=True)

class StrategicDirection(models.Model):
    strategy_id = models.AutoField(primary_key=True)
    objective = models.TextField(blank=True, null=True)
    strategic_alignment = models.TextField(blank=True, null=True)
    kpi = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, related_name='strategy_owner', blank=True, null=True, on_delete=models.SET_NULL)
    resources_allocated = models.TextField(blank=True, null=True)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    last_review_date = models.DateField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    supporting_documents = models.FileField(upload_to='strategy_documents/')
    comments = models.TextField(blank=True, null=True)

class ResourceManagement(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_type = models.CharField(max_length=255)
    allocated_to = models.ForeignKey(Staff, related_name='allocated_to', blank=True, null=True, on_delete=models.SET_NULL)
    allocation_date = models.DateField(blank=True, null=True)
    risk_assessment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, related_name='resource_owner', blank=True, null=True, on_delete=models.SET_NULL)
    utilization_metrics = models.TextField(blank=True, null=True)
    compliance_status = models.CharField(max_length=50, choices=[('Compliant', 'Compliant'), ('Partially Compliant', 'Partially Compliant'), ('Non-Compliant', 'Non-Compliant')])
    last_audit_date = models.DateField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='resource_documents/')
    comments = models.TextField(blank=True, null=True)

class RiskAndCompliance(models.Model):
    risk_compliance_id = models.AutoField(primary_key=True)
    risk_name = models.CharField(max_length=255)
    risk_severity =  models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    regulatory_requirement = models.TextField(blank=True, null=True)
    compliance_status = models.CharField(max_length=50, choices=[('Compliant', 'Compliant'), ('Partially Compliant', 'Partially Compliant'), ('Non-Compliant', 'Non-Compliant')])
    owner = models.ForeignKey(Staff, related_name='risk_owner', blank=True, null=True, on_delete=models.SET_NULL)
    last_review_date = models.DateField(blank=True, null=True)
    improvement_actions = models.TextField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='risk_documents/')
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    comments = models.TextField(blank=True, null=True)

class PerformanceReporting(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=255)
    reporting_period = models.TextField(blank=True, null=True)
    kpis_assessed = models.TextField(blank=True, null=True)
    performance_summary = models.TextField(blank=True, null=True)
    prepared_by = models.ForeignKey(Staff, related_name='prepared_by', blank=True, null=True, on_delete=models.SET_NULL)
    approved_by = models.ForeignKey(Staff, related_name='performance_approved_by', blank=True, null=True, on_delete=models.SET_NULL)
    distribution_list = models.TextField(blank=True, null=True)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
    supporting_documents = models.FileField(upload_to='performance_documents/')
    comments = models.TextField(blank=True, null=True)

class StakeholderEngagement(models.Model):
    stakeholder_id = models.AutoField(primary_key=True)
    stakeholder_group = models.CharField(max_length=255)
    engagement_type = models.TextField(blank=True, null=True)
    feedback_collected = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)
    communication_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(Staff, related_name='stakeholder_owner', blank=True, null=True, on_delete=models.SET_NULL)
    key_issues = models.TextField(blank=True, null=True)
    resolution_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    supporting_documents = models.FileField(upload_to='stakeholder_documents/')
    comments = models.TextField(blank=True, null=True)

class EthicalGovernance(models.Model):
    ethics_id = models.AutoField(primary_key=True)
    code_of_conduct_reference = models.TextField(blank=True, null=True)
    incident_type = models.CharField(max_length=255)
    incident_reported_by = models.ForeignKey(Staff, related_name='incident_reported_by', blank=True, null=True, on_delete=models.SET_NULL)
    resolution_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    responsible_owner = models.ForeignKey(Staff, related_name='responsible_owner', blank=True, null=True, on_delete=models.SET_NULL)
    follow_up_actions = models.TextField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='ethics_documents/')
    comments = models.TextField(blank=True, null=True)
    ethical_risk_rating = models.TextField(blank=True, null=True)

class GovernanceImprovement(models.Model):
    improvement_id = models.AutoField(primary_key=True)
    initiative_name = models.CharField(max_length=255)
    improvement_objective = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, related_name='improvement_owner', blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField(blank=True, null=True)
    target_completion_date = models.DateField(blank=True, null=True)
    progress_status =  models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    resources_allocated = models.TextField(blank=True, null=True)
    impact_assessment = models.TextField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='improvement_documents/')
    comments = models.TextField(blank=True, null=True)

class GovernanceDocumentManagement(models.Model):
    document_id = models.AutoField(primary_key=True)
    document_title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Staff, related_name='uploaded_by', blank=True, null=True, on_delete=models.SET_NULL)
    upload_date = models.DateField(blank=True, null=True)
    version = models.CharField(max_length=50)
    document_type = models.CharField(max_length=255)
    associated_processes = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
   
