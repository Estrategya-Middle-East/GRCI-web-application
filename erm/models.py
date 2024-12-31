from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from main_app.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

# KPI Model (Optional)
class KPI(models.Model):
    kpi_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


###############################################
#                  WorkFlow                   #
###############################################
class Risk(models.Model):
    name = models.CharField(max_length=100, null= True)
    description = models.TextField(null= True)
    workflow_status = models.CharField(max_length=20, default='new', choices=[
        ('new', 'New'),
        ('define', 'Define'),
        ('assessment', 'Assessment'),
        ('prioritization', 'Prioritization'),
        ('response', 'Response'),
        ('residual', 'Residual'),
        ('close', 'Close'),
        ('completed', 'Completed'),
    ])
    define_approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    assessment_approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    prioritization_approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    response_approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    residual_approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    close_approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    
    def __str__(self):
        return self.name



class RiskDefine(models.Model):
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="define_step", default=1)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True)
    #section = models.CharField(max_length=255, blank=True, null=True)
    objective = models.ForeignKey('Objective', on_delete=models.DO_NOTHING, blank=True, null=True)
    identified_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    identification_date= models.DateField(default=now)
    risk_cause= models.TextField(blank=True, null=True)
    risk_event= models.TextField(blank=True, null=True)
    risk_impact= models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('Operational', 'Operational'),
            ('Strategic', 'Strategic'),
            ('Financial', 'Financial'),
            ('Compliance', 'Compliance'),
        ],
        default='Operational',
    )
    subcategory= models.CharField(max_length=255, null=1,blank=1)
    source = models.CharField(
        max_length=50,
        choices=[
            ('Internal', 'Internal'),
            ('External', 'External'),
        ],
        default='Internal',
    )
    likelihood= models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=0,)
    impact= models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=0,)
    risk_score = models.IntegerField(default=0)
    approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    
    def save(self, *args, **kwargs):
        self.risk_score = self.impact * self.likelihood
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Define Risk - {self.risk.name}"


class RiskAss(models.Model):
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="assessment_step", default=1)
    assessment_date = models.DateField(default=now)
    assessed_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    likelihood_rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=0,)
    impact_rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=0,)
    risk_score = models.IntegerField(default=0) 
    residual_risk = models.IntegerField(default=0) 
    risk_heatmap_position =models.CharField(max_length=50,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Severe', 'Severe'),
        ],
        default='Low',)
    mitigation_actions = models.CharField(max_length=255, blank=True, null=True)
    reviewer_comments=models.TextField(blank=True, null=True)
    approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    
    def save(self, *args, **kwargs):
        # Calculate risk score
        self.risk_score = self.impact_rating * self.likelihood_rating
        
        # Determine risk heatmap position
        if self.risk_score <= 4:
            self.risk_heatmap_position = 'Low'
        elif 4 < self.risk_score < 10:
            self.risk_heatmap_position = 'Medium'
        elif 10 <= self.risk_score < 20:
            self.risk_heatmap_position = 'High'
        elif 20 <= self.risk_score <= 25:
            self.risk_heatmap_position = 'Severe'
        
        # Save the instance
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Assessment - {self.risk.name}"

class RiskPrioritization(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical','Critical')
    ]
    REVIEW_FREQUENCY_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually'),
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]
    
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="prioritization_step", default=1)
    risk_score = models.IntegerField(default=0) 
    priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Medium")
    justification = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    next_reviewdate = models.DateField(default=now)
    review_frequency = models.CharField(max_length=50, choices=REVIEW_FREQUENCY_CHOICES, default="Monthly")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Open")
    comments=models.TextField(blank=True, null=True)
    is_manual_edit = models.BooleanField(default=False)
    approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    
    def __str__(self):
        return f"Prioritizationt - {self.risk.name}"
    
@receiver(post_save, sender=RiskAss)
def update_risk_prioritization(sender, instance, **kwargs):
    # Ensure there is a corresponding RiskPrioritization object
    try:
        prioritization = RiskPrioritization.objects.get(risk=instance.risk)
        if not prioritization.is_manual_edit:
            prioritization.risk_score = instance.risk_score
            prioritization.save(update_fields=['risk_score'])
    except RiskPrioritization.DoesNotExist:
        # Optionally create a RiskPrioritization instance if it doesn't exist
        RiskPrioritization.objects.create(
            risk=instance.risk,
            risk_score=instance.risk_score
        )

class RiskResponse(models.Model):
    STRATEGY_CHOICES = [
        ('Avoid', 'Avoid'),
        ('Mitigate', 'Mitigate'),
        ('Transfer', 'Transfer'),
        ('Accept','Accept')
    ]
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="response_step", default=1)
    response_strategy = models.CharField(max_length=50, choices=STRATEGY_CHOICES, default="Avoid")
    ActionPlan = models.TextField(blank=True, null=True)
    responsible_party = models.ManyToManyField(Staff, blank=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)
    progress_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Not Started")
    resources_required=models.TextField(blank=True, null=True)
    effectiveness_review=models.TextField(blank=True, null=True)
    approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    
    def __str__(self):
        return f"Response - {self.risk.name}"

class RiskResidualAss(models.Model):
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="residual_step", default=1)
    assessment_date = models.DateField(default=now)
    assessed_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    risk_appetite = models.ForeignKey('RiskAppetite', on_delete=models.DO_NOTHING, blank=True, null=True)
    likelihood_rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=0,)
    impact_rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=0,)
    risk_score = models.IntegerField(default=0) 
    risk_heatmap_position =models.CharField(max_length=50,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Severe', 'Severe'),
        ],
        default='Low',)
    mitigation_actions = models.CharField(max_length=255, blank=True, null=True)
    reviewer_comments=models.TextField(blank=True, null=True)
    approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    
    def save(self, *args, **kwargs):
        # Calculate risk score
        self.risk_score = self.impact_rating * self.likelihood_rating
        
        # Determine risk heatmap position
        if self.risk_score <= 4:
            self.risk_heatmap_position = 'Low'
        elif 4 < self.risk_score < 10:
            self.risk_heatmap_position = 'Medium'
        elif 10 <= self.risk_score < 20:
            self.risk_heatmap_position = 'High'
        elif 20 <= self.risk_score <= 25:
            self.risk_heatmap_position = 'Severe'
        
        # Save the instance
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Residual Risk Assessment - {self.risk.name}"

class RiskClose(models.Model):
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="close_step", default=1)
    close_date = models.DateField(default=now)
    closed_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(null= True)
    reviewer_comments=models.TextField(blank=True, null=True)
    approval_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )
    

class Oversight(models.Model):
    OversightID = models.AutoField(primary_key=True)
    MeetingDate = models.DateTimeField(blank=True, null=True)
    CommitteeMembers = models.TextField(blank=True, null=True)  # For storing Char array
    MeetingAgenda = models.TextField(blank=True, null=True)
    DecisionsMade = models.TextField(blank=True, null=True)
    ActionItems = models.TextField(blank=True, null=True)  # Char array
    RiskTopicsDiscussed = models.TextField(blank=True, null=True)  # Char array
    FollowUpActions = models.CharField(blank=True, null=True)  # Char array
    SupportingDocuments = models.FileField(upload_to='oversight_docs/', blank=True, null=True)  # File pointer
    MeetingMinutes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Oversight ID {self.OversightID}"
    
class OperatingStructure(models.Model):
    StructureID = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=255)
    RoleName = models.CharField(max_length=255)
    Responsibilities = models.TextField(blank=True, null=True)
    RiskOwnership = models.CharField(blank=True, null=True)  
    ReportingHierarchy = models.TextField(blank=True, null=True)
    ApprovalMatrix = models.CharField(blank=True, null=True)  
    Status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    BudgetAllocated = models.DecimalField(max_digits=10, decimal_places=2)
    KPITracking = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.DepartmentName} - {self.RoleName}"
    
    
class CultureSurvey(models.Model):
    SurveyID = models.AutoField(primary_key=True)
    SurveyTitle = models.CharField(max_length=255)
    SurveyDate = models.DateTimeField(blank=True, null=True)
    RespondentID = models.ForeignKey(Staff, on_delete=models.CASCADE)  # Assuming you have a Respondent model
    Questions = models.TextField(blank=True, null=True)  # Char array for survey questions
    Responses = models.TextField(blank=True, null=True)  # Char array for responses
    OverallScore = models.DecimalField(max_digits=5, decimal_places=2)
    ImprovementAreas = models.TextField(blank=True, null=True)
    ComplianceIssues = models.BooleanField(default=False,blank=True, null=True)
    SurveyFeedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.SurveyTitle
    


class CoreValuesMonitoring(models.Model):
    MonitoringID = models.AutoField(primary_key=True)
    ViolationType = models.CharField(max_length=255)
    ViolationDescription = models.TextField(blank=True, null=True)
    ReportedBy = models.ForeignKey(Staff, on_delete=models.CASCADE)  # Assuming 'Employee' model exists
    IncidentDate = models.DateTimeField(blank=True, null=True)
    ResolutionActions = models.TextField(blank=True, null=True)
    ComplianceCheckDate = models.DateTimeField(blank=True, null=True)
    ComplianceStatus = models.CharField(max_length=15, choices=[('Compliant', 'Compliant'), ('Non-Compliant', 'Non-Compliant')])
    FollowUpRequired = models.BooleanField(default=False)
    SupportingEvidence = models.FileField(upload_to='corevaluesmonitoring_docs/', blank=True, null=True)  # File pointer

    def __str__(self):
        return f"Monitoring ID {self.MonitoringID} - {self.ViolationType}"


class RiskTalent(models.Model):
    TalentID = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=255)
    Role = models.CharField(max_length=255)
    TrainingPrograms = models.TextField(blank=True, null=True)  # List of training programs (Char array)
    Certifications = models.TextField(blank=True, null=True)  # List of certifications (Char array)
    RiskExperienceYears = models.DecimalField(max_digits=5, decimal_places=2)  # Years of experience
    PerformanceMetrics = models.TextField(blank=True, null=True)
    LastEvaluationDate = models.DateTimeField(blank=True, null=True)
    SkillsGap = models.TextField(blank=True, null=True)
    DevelopmentPlan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.EmployeeName} - {self.Role}"
    
# Strategic Planning and Goal Alignment
class BusinessContext(models.Model):
    context_id = models.AutoField(primary_key=True)
    internal_factors = models.TextField(null=True, blank=True)
    external_factors = models.TextField(null=True, blank=True)
    swot_strengths = models.TextField(null=True, blank=True)
    swot_weaknesses = models.TextField(null=True, blank=True)
    swot_opportunities = models.TextField(null=True, blank=True)
    swot_threats = models.TextField(null=True, blank=True)
    pestle_political = models.TextField(null=True, blank=True)
    pestle_economic = models.TextField(null=True, blank=True)
    pestle_social = models.TextField(null=True, blank=True)
    pestle_technological = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Business Context {self.context_id}"
    

class RiskAppetite(models.Model):
    REVIEW_CYCLE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually')
    ]

    appetite_id = models.AutoField(primary_key=True)
    risk_tolerance_level = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    linked_objectives = models.TextField(null=True, blank=True)  # Django 3.1+ supports TextField
    risk_thresholds = models.TextField(null=True, blank=True)
    risk_appetite_statement = models.TextField(null=True, blank=True)
    approved_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    review_cycle = models.CharField(max_length=10, choices=REVIEW_CYCLE_CHOICES, null=True, blank=True)
    deviation_actions = models.TextField(null=True, blank=True)
    supporting_evidence = models.FileField(upload_to='risk_appetite_docs/', null=True, blank=True)

    def __str__(self):
        return self.risk_thresholds


class StrategicEvaluation(models.Model):
    evaluation_id = models.AutoField(primary_key=True)
    strategy_details = models.TextField(null=True, blank=True)
    linked_risks = models.TextField(null=True, blank=True)  # Text Array for associated risks
    alternative_strategies = models.TextField(null=True, blank=True)  # Text Array for alternative strategies
    impact_assessment = models.TextField(null=True, blank=True)
    cost_benefit_analysis = models.TextField(null=True, blank=True)
    kpis = models.TextField(null=True, blank=True)  # KPIs as a plain text field (or use TextField if structure needed)
    evaluation_date = models.DateTimeField(null=True, blank=True)
    evaluation_outcome = models.TextField(null=True, blank=True)
    reviewer_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Evaluation {self.evaluation_id}"

    
    
class Objective(models.Model):
    PROGRESS_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    id = models.AutoField(primary_key=True, unique=True)
    objective_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    linked_risks = models.TextField(null=True, blank=True)  # Text Array for associated risks
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    responsible_parties = models.TextField(null=True, blank=True)  # Text Array for individuals/teams
    kpis = models.TextField(null=True, blank=True)  # Text Array for key performance indicators
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True)
    progress_status = models.CharField(max_length=20, choices=PROGRESS_STATUS_CHOICES)

    def __str__(self):
        return self.objective_name
    
# Continuous Monitoring and Optimization
class ChangeAssessment(models.Model):
    CHANGE_TYPE_CHOICES = [
        ('Internal', 'Internal'),
        ('External', 'External')
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    change_id = models.AutoField(primary_key=True)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES)
    change_description = models.TextField(null=True, blank=True)
    affected_risks = models.TextField(null=True, blank=True)  # List of RiskIDs (Text array)
    impact_assessment = models.TextField(null=True, blank=True)
    change_date = models.DateTimeField(null=True, blank=True)
    response_actions = models.TextField(null=True, blank=True)
    responsible_party = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming a User model
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    review_date = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Change Assessment {self.change_id}"
    
class PerformanceReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    objective = models.ForeignKey('Objective', on_delete=models.CASCADE)  # Assuming the Objective model exists
    review_period = models.CharField(max_length=50)
    kpis_assessed = models.TextField(null=True, blank=True)  # List of KPIs assessed (Text array)
    target_values = models.TextField(null=True, blank=True)  # Target values for each KPI (Text array)
    actual_values = models.TextField(null=True, blank=True)  # Actual values achieved for each KPI (Text array)
    variance_analysis = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)
    areas_for_improvement = models.TextField(null=True, blank=True)
    reviewer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming a User model
    review_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Performance Review {self.review_period}"
    
class ImprovementAction(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    improvement_id = models.AutoField(primary_key=True)
    related_risk = models.ForeignKey('Risk', on_delete=models.CASCADE)  # Assuming the Risk model exists
    action_description = models.TextField(null=True, blank=True)
    initiated_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming the Initiator is a User
    start_date = models.DateTimeField(null=True, blank=True)
    target_completion_date = models.DateTimeField(null=True, blank=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    resources_allocated = models.TextField(null=True, blank=True)
    success_criteria = models.TextField(null=True, blank=True)
    progress_updates = models.TextField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Improvement Action {self.improvement_id}"




    