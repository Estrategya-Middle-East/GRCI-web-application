from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from main_app.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver



# Macro Planning (Annual) #

# 1. Audit Universe
class AuditUniverse(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical','Critical')
    ]
    RANGE_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    audit_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    entity_type = models.CharField(
        max_length=50,
         choices=[
            ('Process', 'Process'),
            ('Unit', 'Unit'),
            ('Program', 'Program'),
            ('Service Line', 'Service Line'),
            ('Function', 'Function'),
        ],
        default='Process',
        
    )
    organizational_category = models.CharField(
        max_length=50,
        choices=[
            ('Department', 'Department'),
            ('Division', 'Division'),
            ('Business Unit', 'Business Unit'),
        ],
        default='Department',
    )
    process_category = models.CharField(
        max_length=50,
        choices=[
            ('Procurement', 'Procurement'),
            ('Asset Management', 'Asset Management'),
            ('Financial Reporting', 'Financial Reporting'),
        ],
        default='Procurement',
    )
    location_category = models.CharField(
        max_length=50,
        choices=[
            ('Headquarters', 'Headquarters'),
            ('Regional Office', 'Regional Office'),
            ('Local Office', 'Local Office'),
        ],
        default='Headquarters',
    )
    risk_category = models.CharField(
        max_length=50,
        choices=[
            ('Operational', 'Operational'),
            ('Strategic', 'Strategic'),
            ('Financial', 'Financial'),
            ('Compliance', 'Compliance'),
        ],
        default='Operational',
    )
    risk_score = models.IntegerField(blank=True, null=True)
    strategic_relevance  = models.CharField(max_length=50, choices=RANGE_CHOICES, default="Medium")
    priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Medium")
    audit_scope = models.TextField(blank=True, null=True)
    last_audit_date = models.DateField(blank=True, null=True)
    next_audit_date = models.DateField(blank=True, null=True)
    assigned_auditor = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    audit_cycle_status = models.CharField(max_length=50, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    senior_manager_feedback = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.entity_name
    
# 2. Risk Assessment
class RiskAssessment(models.Model):
    risk_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    risk_type = models.CharField(
        max_length=50,
        choices=[
            ('Operational', 'Operational'),
            ('Strategic', 'Strategic'),
            ('Financial', 'Financial'),
            ('Compliance', 'Compliance'),
        ],
        default='Operational',
    )    
    inherent_risk = models.IntegerField(blank=True, null=True)
    residual_risk = models.IntegerField(blank=True, null=True)
    control_effectiveness = models.TextField(blank=True, null=True)
    assessed_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)  # Replace with ForeignKey if linked to a user model
    assessed_date = models.DateField(blank=True, null=True)
    risk_severity = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    comments = models.TextField(blank=True, null=True)
  

    def __str__(self):
        return self.entity_name


# 3. Annual Audit Plan (AAP)
class AuditPlan(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical','Critical')
    ]
    FREQUENCY_CHOICES = [
    ('DAILY', 'Daily'),
    ('WEEKLY', 'Weekly'),
    ('MONTHLY', 'Monthly'),
    ('QUARTERLY', 'Quarterly'),
    ('ANNUALLY', 'Annually'),
]
    
    plan_id = models.AutoField(primary_key=True)
    audit_year = models.IntegerField(blank=True, null=True)
    entity_name = models.CharField(max_length=255)
    audit_frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, blank=True, null=True)
    priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Medium")
    allocated_resources = models.TextField(blank=True, null=True)
    audit_schedule = models.TextField(blank=True, null=True)
    assigned_team = models.ManyToManyField(Staff, blank=True)  
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name
    

# Macro Planning (Annual) #

# 4. Audit Assessment
class AuditAssessment(models.Model):
    assessment_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    assigned_team = models.ManyToManyField(Staff, blank=True) 
    scope = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.entity_name


# 5. Audit Notification
class AuditNotification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    auditee_name = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    audit_scope = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    audit_timeline = models.TextField(blank=True, null=True)
    notification_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name
    
# 6. Entrance Meeting
class EntranceMeeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Staff, blank=True)  
    discussion_points = models.TextField(blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name

class ProcessUnderstanding(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
# 7. Sub-Process 
class SubProcess(models.Model):
    process_id = models.ForeignKey(ProcessUnderstanding, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    subprocess_id = models.ForeignKey(SubProcess, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class ProcessRisk(models.Model):
    subprocess_id = models.ForeignKey(SubProcess, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    risk_score = models.IntegerField(blank=True, null=True)
    risk_type = models.CharField(blank=True, null=True,
        max_length=50,
        choices=[
            ('Operational', 'Operational'),
            ('Strategic', 'Strategic'),
            ('Financial', 'Financial'),
            ('Compliance', 'Compliance'),
        ],
        default='Operational',
    )  
    
    def __str__(self):
        return self.name

class control(models.Model):
    subprocess_id = models.ForeignKey(SubProcess, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    performed_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL) 
    performed_date = models.DateField(blank=True, null=True) 
    control_location = models.TextField(max_length=255, blank=True, null=True)
    control_class = models.CharField(blank=True, null=True,
        max_length=50,
        choices=[
            ('Operational', 'Operational'),
            ('Strategic', 'Strategic'),
            ('Financial', 'Financial'),
            ('Compliance', 'Compliance'),
        ],
        default='Operational',
    )   
    control_type = models.CharField(blank=True, null=True,
        max_length=50,
        choices=[
            ('Preventive', 'Preventive'),
            ('Detective', 'Detective'),
            ('Concurrent', 'Concurrent'),
        ],
        default='Preventive',
    )
    final_decision = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return self.name   



# 8. Audit Program
class AuditTest(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Partially Completed', 'Partially Completed'),
        ('Completed', 'Completed'),
    ]
    name = models.CharField(max_length=255)
    subprocess_id = models.ForeignKey(SubProcess, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    tested_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Not Started")
    result = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class AuditProcedure(models.Model):
    name = models.CharField(max_length=255)
    subprocess_id = models.ForeignKey(SubProcess, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    conducted_by = models.ForeignKey(Staff, related_name= "conducted_by", blank=True, null=True, on_delete=models.SET_NULL) 
    
    
    def __str__(self):
        return self.name
        
# 8.1. Requirements List (LOR)
class RequirementsList(models.Model):
    STATUS_CHOICES = [
        ('Not Yet Shared', 'Not Yet Shared'),
        ('Partially Received', 'Partially Received'),
        ('Fully Received', 'Fully Received'),
    ]
    test_id = models.ForeignKey(AuditTest, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    Description = models.TextField(blank=True, null=True)
    requested_by = models.ForeignKey(Staff, related_name= "requested_by", blank=True, null=True,  on_delete=models.SET_NULL)
    escalation_to = models.CharField(max_length=255,blank=True, null=True)
    requested_from = models.CharField(max_length=255,blank=True, null=True)
    date_requested = models.DateField(blank=True, null=True)
    reminder_date = models.DateField(blank=True, null=True)
    date_received = models.DateField(blank=True, null=True)
    escalation = models.BooleanField(blank=True, null=True)
    sla = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Not Yet Shared", blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Fieldwork (Per Audit) #

# 9. Working Paper
class WorkingPaper(models.Model):
    working_paper_id = models.AutoField(primary_key=True)    
    entity_name = models.CharField(max_length=255)
    analytics = models.CharField(
        max_length=50,
        choices=[
            ('Manual', 'Manual'),
            ('CAAT', 'CAAT'),
        ],
        default='Manual',
    )    
    audit_task = models.CharField(max_length=255)
    objective = models.TextField(blank=True, null=True)
    scope = models.TextField(blank=True, null=True)
    sample_justification = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, related_name= "owner", blank=True, null=True, on_delete=models.SET_NULL) 
    test_conclusion = models.TextField(blank=True, null=True)
    evidence_collected = models.TextField(blank=True, null=True)
    performed_by = models.ForeignKey(Staff, related_name= "performed_by", blank=True, null=True, on_delete=models.SET_NULL) 
    reviewed_by = models.ForeignKey(Staff, related_name= "reviewed_by", blank=True, null=True, on_delete=models.SET_NULL) 
    task_start_date = models.DateField(blank=True, null=True)
    task_completion_date = models.DateField(blank=True, null=True)
    observation = models.BooleanField(blank=True, null=True)
    observation_description = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.entity_name

# 10. Observation Sheet
class ObservationSheet(models.Model):
    observation_id = models.AutoField(primary_key=True)    
    entity_name = models.CharField(max_length=255)
    observation_details = models.TextField(blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    deadline = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name
    
# 11. Other Notes
class OtherNotes(models.Model):
    note_id = models.AutoField(primary_key=True)   
    entity_name = models.CharField(max_length=255)
    note_details = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    note_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name


# Reporting (Per Audit) #

# 12. Draft Report
class DraftReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    findings = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    drafted_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    draft_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name

# 13. Exit Meeting
class ExitMeeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Staff, blank=True)  
    discussion_points = models.TextField(blank=True, null=True)
    agreed_actions = models.TextField(blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name

# 14. Final Report
class FinalReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    findings_summary = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    submission_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.entity_name


# Feedback (Per Audit) #

# 15. Feedback
class Feedback(models.Model):
    survey_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    auditee_name =  models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    feedback_details = models.TextField(blank=True, null=True)
    survey_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name


# Follow-Up (Per Audit) #

# 16. Audit Follow-Up
class AuditFollowUp(models.Model):
    follow_up_id = models.AutoField(primary_key=True)
    entity_name = models.CharField(max_length=255)
    issues_resolved = models.TextField(blank=True, null=True)
    corrective_actions = models.TextField(blank=True, null=True)
    follow_up_by =  models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    follow_up_date = models.DateField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.entity_name
    
# Documents Management
class DocumentsManagement(models.Model):
    document_id = models.AutoField(primary_key=True)
    audit_id = models.ForeignKey(AuditUniverse, blank=True, null=True, on_delete=models.SET_NULL)  
    document_title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    upload_date = models.DateField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    access_permissions = models.TextField(blank=True, null=True)
    associated_risks = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    file_link = models.FileField(upload_to='documents/')



