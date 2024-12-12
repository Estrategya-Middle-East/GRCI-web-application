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
    
    def __str__(self):
        return self.name



class RiskDefine(models.Model):
    risk = models.OneToOneField(Risk, on_delete=models.CASCADE, related_name="define_step", default=1)
    department = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    identified_by = models.CharField(max_length=255, blank=True, null=True)
    identification_date= models.DateField(default=now)
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
        default=1,)
    impact= models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=1,)
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
    assessed_by = models.CharField(max_length=255, blank=True, null=True)
    likelihood_rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=1,)
    impact_rating = models.IntegerField(
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ],
        default=1,)
    risk_score = models.IntegerField(default=0) 
    residual_risk = models.IntegerField(default=0) 
    risk_heatmap_position =models.CharField(max_length=50,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
        ],
        default='Low',)
    mitigation_actions = models.CharField(max_length=255, blank=True, null=True)
    reviewer_comments=models.TextField(null= True)
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
        self.risk_score = self.impact_rating * self.likelihood_rating
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
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    next_reviewdate = models.DateField(default=now)
    review_frequency = models.CharField(max_length=50, choices=REVIEW_FREQUENCY_CHOICES, default="Monthly")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Open")
    comments=models.TextField(null= True)
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
    ActionPlan = models.TextField(null= True)
    responsible_party = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)
    progress_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Not Started")
    resources_required=models.TextField(null= True)
    effectiveness_review=models.TextField(null= True)
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
        return f"Risk Appetite {self.appetite_id}"


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




##############################################################
# old Models #################################################
##############################################################
""" class Objective(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    PROGRESS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    #department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=now)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Active")
    priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Medium")
    kpis_linked = models.ManyToManyField(KPI)
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    progress_status = models.CharField(
        max_length=50, choices=PROGRESS_CHOICES, default="Not Started"
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class ObjectiveStrategy(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    strategy_name = models.CharField(max_length=255)
    strategy_description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    timeline = models.DateField(default=now)
    
    def __str__(self):
        return self.name


class ObjectiveProgress(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    progress_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0.0)
    last_updated = models.DateTimeField(default=now)  # Removed auto_now=True
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


# Inherent Risk Models
class InherentRisk(models.Model):
    RISK_LIKELIHOOD_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    ]

    RISK_IMPACT_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Very High', 'Very High'),
    ]

    RISK_TYPE_CHOICES = [
        ('Operational', 'Operational'),
        ('Strategic', 'Strategic'),
        ('Financial', 'Financial'),
        ('Compliance', 'Compliance'),
    ]

    REVIEW_FREQUENCY_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually'),
    ]

    risk_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    likelihood = models.CharField(max_length=50, choices=RISK_LIKELIHOOD_CHOICES, default="Low")
    impact = models.CharField(max_length=50, choices=RISK_IMPACT_CHOICES, default="Low")
    score = models.FloatField(default=0.0)
    creation_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    associated_objective = models.ForeignKey(Objective, on_delete=models.SET_NULL, null=True, blank=True)
    source_of_risk = models.TextField(blank=True, null=True)
    date_identified = models.DateField(default=now)
    risk_type = models.CharField(max_length=50, choices=RISK_TYPE_CHOICES, default="Operational")
    current_controls = models.TextField(blank=True, null=True)
    review_frequency = models.CharField(max_length=50, choices=REVIEW_FREQUENCY_CHOICES, default="Monthly")
    rish_event = models.TextField(blank=True, null=True)
    rish_cause = models.TextField(blank=True, null=True)
    rish_impact = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class RiskAssessment(models.Model):
    assessment_id = models.AutoField(primary_key=True, unique=True)
    risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    assessment_date = models.DateField(default=now)
    assessed_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    risk_value = models.FloatField(default=0.0)
    probability_score = models.IntegerField(default=0)
    impact_score = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

@receiver(post_save , sender=InherentRisk)
def create_risk_assessment(sender,instance,created , **kwargs):
    if created:
        RiskAssessment.objects.create(
            risk = instance,
            risk_value = instance.score,
            assessed_by = instance.owner,
        )

# Key Risk Indicator Models
class KeyRiskIndicator(models.Model):
    kri_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    related_risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    threshold_lower = models.FloatField(default=0.0)
    threshold_upper = models.FloatField(default=0.0)
    current_value = models.FloatField(default=0.0)
    measurement_frequency = models.CharField(
        max_length=50,
        choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')],
        default="Monthly",
    )
    responsible_person = models.CharField(
        max_length=255,
        blank=True, 
        null=True,  # Allow null for existing rows
        default="Unassigned"  # Provide a default value
    )
    data_source = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    alert_triggers = models.CharField(
        max_length=50,
        choices=[('Email Alert', 'Email Alert'), ('Dashboard Notification', 'Dashboard Notification')],
        default="Email Alert",
    ) 
    status = models.CharField(
        max_length=50,
        choices=[('Active', 'Active'), ('Inactive', 'Inactive')],
        default="Active",
    ) 
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

@receiver(post_save , sender=InherentRisk)
def create_key_metric(sender,instance,created , **kwargs):
    if created:
        KeyRiskIndicator.objects.create(
            related_risk = instance,
            owner = instance.owner,
            name = f"{instance} Indicator",
            responsible_person = f"{instance.owner}",
            current_value = instance.score,
            status = "Inactive"
        )

class KeyMetric(models.Model):
    metric_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    related_kri = models.ForeignKey(KeyRiskIndicator, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(default=now)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
@receiver(post_save , sender=KeyRiskIndicator)
def create_key_metric(sender,instance,created , **kwargs):
    if created:
        KeyMetric.objects.create(
            related_kri = instance,
            name = str(instance) + " Key Metric"
        )

# Risk Appetite Console
class RiskAppetite(models.Model):
    appetite_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    min_threshold = models.FloatField(default=0.0)
    max_threshold = models.FloatField(default=0.0)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    approving_authority = models.CharField(max_length=255)
    review_date = models.DateField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class RiskTolerance(models.Model):
    tolerance_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    related_appetite = models.ForeignKey(RiskAppetite, on_delete=models.CASCADE)
    related_risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    accepted_tolerance_level = models.IntegerField(default=0)
    monitoring_mechanism = models.TextField(blank=True, null=True)
    current_status = models.CharField(
        max_length=50,
        choices=[('Within Tolerance', 'Within Tolerance'), ('Out of Tolerance', 'Out of Tolerance'),],
        default="Within Tolerance",
    )
    review_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Control
class Control(models.Model):
    control_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    related_risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    implementation_date = models.DateField(default=now)
    review_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    assessment_frequency = models.CharField(
        max_length=50,
        choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annually', 'Annually')],
        blank=True,
        null=True,
    )
    control_type = models.CharField(
        max_length=50,
        choices=[('Preventive', 'Preventive'), ('Detective', 'Detective'), ('Corrective', 'Corrective')],
        blank=True,
        null=True,
    )
    control_strength = models.CharField(
        max_length=50,
        choices=[('Strong', 'Strong'), ('Adequate', 'Adequate'), ('Weak', 'Weak')],
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.name

class ControlAssessment(models.Model):
    assessment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    related_control = models.ForeignKey(Control, on_delete=models.CASCADE)
    assessed_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    assessment_date = models.DateField(default=now)
    comments = models.TextField(blank=True, null=True)
    effectiveness_rating = models.CharField(
        max_length=50,
        choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Fair', 'Fair'), ('Poor', 'Poor')],
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.name

class ControlLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    activity = models.CharField(blank=True, null=True)
    related_control = models.ForeignKey(Control, on_delete=models.CASCADE)
    performed_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    timestamp = models.DateField(default=now)
    
    def __str__(self):
        return self.name    


# Residual Risk
class ResidualRisk(models.Model):
    RISK_RATING_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    residual_risk_id = models.AutoField(primary_key=True)
    related_inherent_risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    mitigation_actions = models.TextField(blank=True, null=True)
    current_score = models.FloatField(default=0.0)
    last_review_date = models.DateField(blank=True, null=True)
    updated_score = models.FloatField(default=0.0)
    next_review_date = models.DateField(blank=True, null=True)
    responsible_party = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    residual_risk_rating = models.CharField(
        max_length=50, choices=RISK_RATING_CHOICES, default="Low"
    )

    def __str__(self):
        return f"Residual Risk: {self.related_inherent_risk}"
    
#Residual_Risk_Assessment
class ResidualRiskAssessment(models.Model):
    RISK_RATING_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    assessment_id = models.AutoField(primary_key=True)
    related_residual_risk = models.ForeignKey(ResidualRisk, on_delete=models.CASCADE)
    updated_risk_value = models.FloatField(default=0.0)
    assessment_date = models.DateField(default=now)
    assessed_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_risk_rating = models.CharField(
        max_length=50, choices=RISK_RATING_CHOICES, default="Low"
    )

    def __str__(self):
        return f"Assessment: {self.related_residual_risk}"


# Remediation Actions
class RemediationAction(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    action_id = models.AutoField(primary_key=True)
    related_risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    action_description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(default=now)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Not Started")
    progress_percentage = models.FloatField(default=0.0)
    completion_date = models.DateField(blank=True, null=True)
    associated_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.action_description

class ActionLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    related_action = models.ForeignKey(RemediationAction, on_delete=models.CASCADE)
    activity = models.CharField(blank=True, null=True)
    performed_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    timestamp = models.DateField(default=now)
    
    def __str__(self):
        return self.activity   

# Risk Radar
class RiskRadar(models.Model):
    ZONE_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    COLOR_CHOICES = [
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Red', 'Red'),
    ]

    radar_id = models.AutoField(primary_key=True)
    related_risk = models.ForeignKey(InherentRisk, on_delete=models.CASCADE)
    related_action = models.ForeignKey(RemediationAction, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    last_updated = models.DateField(default=now)
    zone = models.CharField(max_length=100, choices=ZONE_CHOICES, default="Low")
    color = models.CharField(max_length=100, choices=COLOR_CHOICES, default="Green")

    def __str__(self):
        return self.description """
    