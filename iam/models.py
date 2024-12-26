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

# 1. Audit Planning
class AuditPlanning(models.Model):
    plan_id = models.AutoField(primary_key=True)
    audit_year = models.IntegerField(blank=True, null=True)
    risk_assessment_summary = models.TextField(blank=True, null=True)
    planned_audits = models.TextField(blank=True, null=True)
    allocated_resources = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])
    approval_date = models.DateField(blank=True, null=True)
    reviewer_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to a user model
    key_risks = models.TextField(blank=True, null=True)
    audit_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

# 2. Audit Universe Register
class AuditUniverseRegister(models.Model):
    entity_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    risk_score = models.IntegerField(blank=True, null=True)
    control_effectiveness = models.TextField(blank=True, null=True)
    audit_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True)
    last_audit_date = models.DateField(blank=True, null=True)
    next_audit_date = models.DateField(blank=True, null=True)
    risk_owner = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    audit_cycle_status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.entity_name

# 3. Risk Mapping
class RiskMapping(models.Model):
    process_id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=255)
    mapped_risks = models.TextField(blank=True, null=True)
    linked_controls = models.TextField(blank=True, null=True)
    owner_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to a user model
    reviewed_date = models.DateField(blank=True, null=True)
    update_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True)
    risk_severity = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    control_effectiveness = models.TextField(blank=True, null=True)
    documentation_links = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

# 4. Engagement Planning
class EngagementPlanning(models.Model):
    engagement_id = models.AutoField(primary_key=True)
    scope = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    planned_start_date = models.DateField(blank=True, null=True)
    planned_end_date = models.DateField(blank=True, null=True)
    assigned_auditors = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ManyToManyField if linked to a user model
    risk_focus_areas = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2)
    milestones = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.scope


# 5. Audit Resource Planner
class AuditResourcePlanner(models.Model):
    resource_id = models.AutoField(primary_key=True)
    team_member = models.CharField(max_length=255)
    assigned_tasks = models.TextField(blank=True, null=True)
    availability_status = models.CharField(max_length=50, choices=[('Available', 'Available'), ('Busy', 'Busy')])
    skillset = models.TextField(blank=True, null=True)
    allocation_date = models.DateField(blank=True, null=True)
    engagement_id = models.ForeignKey(EngagementPlanning, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to EngagementPlanning
    hours_allocated = models.IntegerField(blank=True, null=True)
    remaining_capacity = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

# 6. Execution Log
class ExecutionLog(models.Model):
    execution_id = models.AutoField(primary_key=True)
    engagement_id = models.ForeignKey(EngagementPlanning, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to EngagementPlanning
    audit_criteria = models.TextField(blank=True, null=True)
    collected_evidence = models.TextField(blank=True, null=True)
    findings_summary = models.TextField(blank=True, null=True)
    exceptions = models.TextField(blank=True, null=True)
    root_cause_analysis = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Open', 'Open'), ('Closed', 'Closed')])
    completion_date = models.DateField(blank=True, null=True)
    follow_up_required = models.BooleanField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

# 7. Follow-Up
class FollowUp(models.Model):
    follow_up_id = models.AutoField(primary_key=True)
    audit_id = models.ForeignKey(AuditUniverseRegister, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to AuditPlanning
    recommendation = models.TextField(blank=True, null=True)
    action_plan = models.TextField(blank=True, null=True)
    assigned_to =  models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    due_date = models.DateField(blank=True, null=True)
    completion_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    review_date = models.DateField(blank=True, null=True)
    effectiveness_rating = models.IntegerField(blank=True, null=True)
    reviewer_comments = models.TextField(blank=True, null=True)
    supporting_documents = models.FileField(upload_to='follow_up_documents/')

# 8. Audit Report
class AuditReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    audit_id = models.ForeignKey(AuditUniverseRegister, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to AuditPlanning
    report_title = models.CharField(max_length=255)
    findings_summary = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    stakeholder_distribution = models.TextField(blank=True, null=True)
    report_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    key_metrics = models.TextField(blank=True, null=True)
    follow_up_plan = models.TextField(blank=True, null=True)
    attached_files = models.FileField(upload_to='audit_reports/')

# 9. Risk Trends Report
class RiskTrendsReport(models.Model):
    trend_id = models.AutoField(primary_key=True)
    recurring_issues = models.TextField(blank=True, null=True)
    root_causes = models.TextField(blank=True, null=True)
    impact_level = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    recommendations = models.TextField(blank=True, null=True)
    metrics = models.TextField(blank=True, null=True)
    associated_audits = models.TextField(blank=True, null=True)
    trend_analysis_date = models.DateField(blank=True, null=True)
    improvement_plan = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)

# 10. Quality Assurance
class QualityAssurance(models.Model):
    qa_id = models.AutoField(primary_key=True)
    assessment_type = models.CharField(max_length=255)
    audit_id = models.ForeignKey(AuditUniverseRegister, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to AuditPlanning
    compliance_status = models.CharField(max_length=50, choices=[('Compliant', 'Compliant'), ('Partially Compliant', 'Partially Compliant'), ('Non-Compliant', 'Non-Compliant')])
    improvement_opportunities = models.TextField(blank=True, null=True)
    reviewer_id = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to a user model
    assessment_date = models.DateField(blank=True, null=True)
    action_plan = models.TextField(blank=True, null=True)
    implementation_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Implemented', 'Implemented')])
    follow_up_date = models.DateField(blank=True, null=True)
    review_summary = models.TextField(blank=True, null=True)

# 11. Fraud Investigation Log
class FraudInvestigationLog(models.Model):
    investigation_id = models.AutoField(primary_key=True)
    suspected_fraud_type = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    reported_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    evidence_collected = models.TextField(blank=True, null=True)
    root_cause = models.TextField(blank=True, null=True)
    corrective_actions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('Open', 'Open'), ('Resolved', 'Resolved')])
    resolution_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    supporting_files = models.FileField(upload_to='fraud_investigations/')

# 12. Document Management
class DocumentManagement(models.Model):
    document_id = models.AutoField(primary_key=True)
    audit_id = models.ForeignKey(AuditUniverseRegister, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to AuditPlanning
    document_title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    upload_date = models.DateField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    access_permissions = models.TextField(blank=True, null=True)
    associated_risks = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    file_link = models.FileField(upload_to='documents/')

# 13. Compliance Tracker
class ComplianceTracker(models.Model):
    compliance_id = models.AutoField(primary_key=True)
    audit_finding = models.TextField(blank=True, null=True)
    regulation_reference = models.TextField(blank=True, null=True)
    compliance_status = models.CharField(max_length=50, choices=[('Compliant', 'Compliant'), ('Partially Compliant', 'Partially Compliant'), ('Non-Compliant', 'Non-Compliant')])
    corrective_actions = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    assigned_owner = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    review_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True)
    last_review_date = models.DateField(blank=True, null=True)
    compliance_rating = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    comments = models.TextField(blank=True, null=True)
