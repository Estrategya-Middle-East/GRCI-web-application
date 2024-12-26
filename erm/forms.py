from django import forms
from django.core.exceptions import ValidationError
from .models import *
import json
from django.forms.widgets import DateInput


class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['name', 'description', ]



class RiskDefineForm(forms.ModelForm):
    class Meta:
        model = RiskDefine
        fields = ['source', 'category', 'subcategory', 'likelihood', 'impact', 'risk_score','identified_by' , 'identification_date', ]
        
        widgets = {
            'identification_date': forms.DateInput(attrs={'type': 'date'}),
            }

class RiskAssForm(forms.ModelForm):
    class Meta:
        model = RiskAss
        fields = ['assessment_date', 'assessed_by', 'likelihood_rating', 'impact_rating', 'risk_score', 'risk_heatmap_position', 'residual_risk', 'mitigation_actions', 'reviewer_comments']

        widgets = {
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            }

class RiskPrioritizationForm(forms.ModelForm):
    class Meta:
        model = RiskPrioritization
        fields = ['risk_score', 'is_manual_edit', 'priority_level', 'justification', 'assigned_to', 'risk_score', 'review_frequency', 'next_reviewdate', 'comments', 'status']

        widgets = {
            'next_reviewdate': forms.DateInput(attrs={'type': 'date'}),
            }

class RiskResponseForm(forms.ModelForm):
    class Meta:
        model = RiskResponse
        fields = ['response_strategy', 'ActionPlan', 'responsible_party', 'start_date', 'end_date', 'progress_status', 'resources_required', 'effectiveness_review']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            }

class OversightForm(forms.ModelForm):
    class Meta:
        model = Oversight
        fields = [
            'MeetingDate',
            'CommitteeMembers',
            'MeetingAgenda',
            'DecisionsMade',
            'ActionItems',
            'RiskTopicsDiscussed',
            'FollowUpActions',
            'MeetingMinutes'
        ]
        widgets = {
            'MeetingDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'CommitteeMembers': forms.Textarea(attrs={'rows': 2}),
            'ActionItems': forms.Textarea(attrs={'rows': 2}),
            'RiskTopicsDiscussed': forms.Textarea(attrs={'rows': 2}),
            'FollowUpActions': forms.Textarea(attrs={'rows': 2}),
            'MeetingMinutes': forms.Textarea(attrs={'rows': 2}),
        }

class OperatingStructureForm(forms.ModelForm):
    class Meta:
        model = OperatingStructure
        fields = [
            'DepartmentName',
            'RoleName',
            'Responsibilities',
            'RiskOwnership',
            'ReportingHierarchy',
            'ApprovalMatrix',
            'Status',
            'BudgetAllocated',
            'KPITracking'
        ]
        widgets = {
            'Responsibilities': forms.Textarea(attrs={'rows': 2}),
            'KPITracking': forms.Textarea(attrs={'rows': 2}),
            'ReportingHierarchy': forms.Textarea(attrs={'rows': 2}),
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')]),
            
        }

    
    
class CultureSurveyForm(forms.ModelForm):
    class Meta:
        model = CultureSurvey
        fields = [
            'SurveyTitle',
            'SurveyDate',
            'RespondentID',
            'Questions',
            'Responses',
            'OverallScore'
        ]
        widgets = {
            'SurveyDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'Questions': forms.Textarea(attrs={'rows': 3}),
            'Responses': forms.Textarea(attrs={'rows': 3}),

        }

  
class CoreValuesMonitoringForm(forms.ModelForm):
    class Meta:
        model = CoreValuesMonitoring
        fields = [
            'ViolationType',
            'ViolationDescription',
            'ReportedBy',
            'IncidentDate',
            'ResolutionActions',
            'ComplianceCheckDate',
            'ComplianceStatus',
            'FollowUpRequired',
            #'SupportingEvidence'
        ]
        widgets = {
            'ViolationDescription': forms.Textarea(attrs={'rows': 2}),
            'ResolutionActions': forms.Textarea(attrs={'rows': 2}),
            'IncidentDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ComplianceCheckDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    #def clean_ViolationDescription(self):
    #    data = self.cleaned_data.get('ViolationDescription')
    #    if data and len(data) < 3:  # Example validation check
    #        raise forms.ValidationError("Violation description should be at least 10 characters long.")
    #    return data


class RiskTalentForm(forms.ModelForm):
    class Meta:
        model = RiskTalent
        fields = [
            'EmployeeName',
            'Role',
            'TrainingPrograms',
            'Certifications',
            'RiskExperienceYears',
            'PerformanceMetrics',
            'LastEvaluationDate',
            'SkillsGap',
            'DevelopmentPlan'
        ]
        widgets = {
            'PerformanceMetrics': forms.Textarea(attrs={'rows': 2}),
            'SkillsGap': forms.Textarea(attrs={'rows': 2}),
            'DevelopmentPlan': forms.Textarea(attrs={'rows': 2}),
            'TrainingPrograms': forms.Textarea(attrs={'rows': 2}),
            'Certifications': forms.Textarea(attrs={'rows': 2}),
            'LastEvaluationDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Strategic Planning and Goal Alignment

class BusinessContextForm(forms.ModelForm):
    class Meta:
        model = BusinessContext
        fields = [
            'internal_factors',
            'external_factors',
            'swot_strengths',
            'swot_weaknesses',
            'swot_opportunities',
            'swot_threats',
            'pestle_political',
            'pestle_economic',
            'pestle_social',
            'pestle_technological',
        ]
        widgets = {
            'internal_factors': forms.Textarea(attrs={'rows': 3}),
            'external_factors': forms.Textarea(attrs={'rows': 3}),
            'swot_strengths': forms.Textarea(attrs={'rows': 3}),
            'swot_weaknesses': forms.Textarea(attrs={'rows': 3}),
            'swot_opportunities': forms.Textarea(attrs={'rows': 3}),
            'swot_threats': forms.Textarea(attrs={'rows': 3}),
            'pestle_political': forms.Textarea(attrs={'rows': 3}),
            'pestle_economic': forms.Textarea(attrs={'rows': 3}),
            'pestle_social': forms.Textarea(attrs={'rows': 3}),
            'pestle_technological': forms.Textarea(attrs={'rows': 3}),
        }
        
class RiskAppetiteForm(forms.ModelForm):
    class Meta:
        model = RiskAppetite
        fields = [
            'risk_tolerance_level',
            'linked_objectives',
            'risk_thresholds',
            'risk_appetite_statement',
            'approved_by',
            'approval_date',
            'review_cycle',
            'deviation_actions',
            #'supporting_evidence'
        ]
        widgets = {
            'linked_objectives': forms.Textarea(attrs={'rows': 3}),
            'risk_thresholds': forms.Textarea(attrs={'rows': 2}),
            'risk_appetite_statement': forms.Textarea(attrs={'rows': 3}),
            'deviation_actions': forms.Textarea(attrs={'rows': 2}),
            'approval_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # You can add validation like this (example: ensure risk tolerance level is positive):
    def clean_risk_tolerance_level(self):
        data = self.cleaned_data.get('risk_tolerance_level')
        if data is not None and data <= 0:
            raise forms.ValidationError("Risk tolerance level must be greater than 0.")
        return data
    
    
class StrategicEvaluationForm(forms.ModelForm):
    class Meta:
        model = StrategicEvaluation
        fields = [
            'strategy_details',
            'linked_risks',
            'alternative_strategies',
            'impact_assessment',
            'cost_benefit_analysis',
            'kpis',
            'evaluation_date',
            'evaluation_outcome',
            'reviewer_comments'
        ]
        widgets = {
            'strategy_details': forms.Textarea(attrs={'rows': 3}),
            'linked_risks': forms.Textarea(attrs={'rows': 3}),
            'alternative_strategies': forms.Textarea(attrs={'rows': 3}),
            'impact_assessment': forms.Textarea(attrs={'rows': 3}),
            'cost_benefit_analysis': forms.Textarea(attrs={'rows': 3}),
            'kpis': forms.Textarea(attrs={'rows': 3}),
            'evaluation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'evaluation_outcome': forms.Textarea(attrs={'rows': 3}),
            'reviewer_comments': forms.Textarea(attrs={'rows': 3}),
        }
 

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = [
            'objective_name',
            'description',
            'linked_risks',
            'start_date',
            'end_date',
            'responsible_parties',
            'kpis',
            'budget_allocated',
            'progress_status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'linked_risks': forms.Textarea(attrs={'rows': 3}),
            'responsible_parties': forms.Textarea(attrs={'rows': 3}),
            'kpis': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'progress_status': forms.Select(choices=Objective.PROGRESS_STATUS_CHOICES),
        }


#Continuous Monitoring and Optimization

class ChangeAssessmentForm(forms.ModelForm):
    class Meta:
        model = ChangeAssessment
        fields = [
            'change_type',
            'change_description',
            'affected_risks',
            'impact_assessment',
            'change_date',
            'response_actions',
            'responsible_party',
            'status',
            'review_date',
            'comments'
        ]
        widgets = {
            'change_description': forms.Textarea(attrs={'rows': 3}),
            'affected_risks': forms.Textarea(attrs={'rows': 3}),
            'impact_assessment': forms.Textarea(attrs={'rows': 3}),
            'response_actions': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'change_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'review_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'objective',
            'review_period',
            'kpis_assessed',
            'target_values',
            'actual_values',
            'variance_analysis',
            'achievements',
            'areas_for_improvement',
            'reviewer',
            'review_date',
        ]
        widgets = {
            'kpis_assessed': forms.Textarea(attrs={'rows': 3}),
            'target_values': forms.Textarea(attrs={'rows': 3}),
            'actual_values': forms.Textarea(attrs={'rows': 3}),
            'variance_analysis': forms.Textarea(attrs={'rows': 3}),
            'achievements': forms.Textarea(attrs={'rows': 3}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 3}),
            'review_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        

class ImprovementActionForm(forms.ModelForm):
    class Meta:
        model = ImprovementAction
        fields = [
            'related_risk',
            'action_description',
            'initiated_by',
            'start_date',
            'target_completion_date',
            'current_status',
            'resources_allocated',
            'success_criteria',
            'progress_updates',
            'completion_date'
        ]
        widgets = {
            'action_description': forms.Textarea(attrs={'rows': 3}),
            'resources_allocated': forms.Textarea(attrs={'rows': 3}),
            'success_criteria': forms.Textarea(attrs={'rows': 3}),
            'progress_updates': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'target_completion_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'completion_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


########################################
########################################
##### old forms ########################
########################################
########################################
########################################


""" class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = [
            'name',
            'description',
            'owner',
            'start_date',
            'end_date',
            'status',
            'priority_level',
            'progress_status',
            'budget_allocated',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['start_date'].initial = instance.start_date
            self.fields['end_date'].initial = instance.end_date
         
class ObjectiveStrategyForm(forms.ModelForm):
    class Meta:
        model = ObjectiveStrategy
        fields = [
            'objective',
            'strategy_name',
            'strategy_description',
            'owner',
            'timeline',
        ]
        widgets = {
            'timeline': forms.DateInput(attrs={'type': 'date'}),
        }


class ObjectiveProgressForm(forms.ModelForm):
    class Meta:
        model = ObjectiveProgress
        fields = [
            'objective',
            'progress_percentage',
            'comments',
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class InherentRiskForm(forms.ModelForm):
    class Meta:
        model = InherentRisk
        fields = [
            'name',
            'description',
            'category',
            'owner',
            'date_identified',
            'likelihood',
            'impact',
            'score',
            'risk_type',
            'source_of_risk',
            'associated_objective',
            'current_controls',
            'review_frequency',
            'rish_cause',
            'rish_impact',
            'rish_event',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'current_controls': forms.Textarea(attrs={'rows': 2}),
            'source_of_risk': forms.Textarea(attrs={'rows': 2}),
            'rish_cause': forms.Textarea(attrs={'rows': 2}),
            'rish_impact': forms.Textarea(attrs={'rows': 2}),
            'rish_event': forms.Textarea(attrs={'rows': 2}),
            'date_identified': forms.DateInput(attrs={'type': 'date'}),
            'likelihood': forms.Select(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Very High', 'Very High')]),
            'impact': forms.Select(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Very High', 'Very High')]),
            'risk_type': forms.Select(choices=[('Operational', 'Operational'), ('Strategic', 'Strategic'), ('Financial', 'Financial'), ('Compliance', 'Compliance')]),
            'review_frequency': forms.Select(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annually', 'Annually')]),
        }


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = [
            'risk',
            'assessment_date',
            'assessed_by',
            'risk_value',
            'probability_score',
            'impact_score',
        ]
        widgets = {
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            }

class KeyRiskIndicatorForm(forms.ModelForm):
    class Meta:
        model = KeyRiskIndicator
        fields = [
            'name',
            'description',
            'related_risk',
            'threshold_lower',
            'threshold_upper',
            'current_value',
            'measurement_frequency',
            'owner',
            'data_source',
            'alert_triggers',
            'status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'threshold_lower': forms.NumberInput(),
            'threshold_upper': forms.NumberInput(),
            'current_value': forms.NumberInput(),
            'measurement_frequency': forms.Select(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')]),
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')]),
            'alert_triggers': forms.Select(choices=[('Email Alert', 'Email Alert'), ('Dashboard Notification', 'Dashboard Notification')]),
        }


class KeyMetricForm(forms.ModelForm):
    class Meta:
        model = KeyMetric
        fields = [
            'name',
            'description',
            'related_kri',
            'date_recorded',
            'comment',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'date_recorded': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),   
        }


# Risk Appetite Console
class RiskAppetiteForm(forms.ModelForm):
    class Meta:
        model = RiskAppetite
        fields = [
            'name',
            'category',
            'description',
            'min_threshold',
            'max_threshold',
            'owner',
            'approving_authority',
            'review_date',
            'comment',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'min_threshold': forms.NumberInput(),
            'max_threshold': forms.NumberInput(),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }


class RiskToleranceForm(forms.ModelForm):
    class Meta:
        model = RiskTolerance
        fields = [
            'name',
            'related_appetite',
            'related_risk',
            'accepted_tolerance_level',
            'monitoring_mechanism',
            'current_status',
            'review_date',
        ]
        widgets = {
            'monitoring_mechanism': forms.Textarea(attrs={'rows': 2}),
            'accepted_tolerance_level': forms.NumberInput(),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Control
class ControlForm(forms.ModelForm):
    class Meta:
        model = Control
        fields = [
            'name',
            'description',
            'related_risk',
            'implementation_date',
            'review_date',
            'owner',
            'control_type',
            'assessment_frequency',
            'control_strength',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'assessment_frequency': forms.Select(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annually', 'Annually')]),
            'control_type': forms.Select(choices=[('Preventive', 'Preventive'), ('Detective', 'Detective'), ('Corrective', 'Corrective')]),
            'control_strength': forms.Select(choices=[('Strong', 'Strong'), ('Adequate', 'Adequate'), ('Weak', 'Weak')]),
            'implementation_date': forms.DateInput(attrs={'type': 'date'}),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ControlAssessmentForm(forms.ModelForm):
    class Meta:
        model = ControlAssessment
        fields = [
            'name',
            'effectiveness_rating',
            'related_control',
            'assessed_by',
            'assessment_date',
            'comments',
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 2}),
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            'effectiveness_rating': forms.Select(choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Fair', 'Fair'), ('Poor', 'Poor')]),
        }


class ControlLogForm(forms.ModelForm):
    class Meta:
        model = ControlLog
        fields = [
            'name',
            'activity',
            'related_control',
            'performed_by',
            'timestamp',
        ]
        
        widgets = {
            'timestamp': forms.DateInput(attrs={'type': 'date'}),
        }
        
# Residual Risk
class ResidualRiskForm(forms.ModelForm):
    class Meta:
        model = ResidualRisk
        fields = [
            'related_inherent_risk',
            'mitigation_actions',
            'current_score',
            'last_review_date',
            'next_review_date',
            'responsible_party',
            'owner',
            'residual_risk_rating',
        ]
        widgets = {
            'mitigation_actions': forms.Textarea(attrs={'rows': 2}),
            'last_review_date': forms.DateInput(attrs={'type': 'date'}),
            'next_review_date': forms.DateInput(attrs={'type': 'date'}),
            'residual_risk_rating': forms.Select(choices=ResidualRisk.RISK_RATING_CHOICES),
        }

class ResidualRiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = ResidualRiskAssessment
        fields = [
            'related_residual_risk',
            'updated_risk_value',
            'assessment_date',
            'assessed_by',
            'updated_risk_rating',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            'updated_risk_rating': forms.Select(choices=ResidualRiskAssessment.RISK_RATING_CHOICES),
        }

# Remediation Action
class RemediationActionForm(forms.ModelForm):
    class Meta:
        model = RemediationAction
        fields = [
            'related_risk',
            'action_description',
            'owner',
            'start_date',
            'due_date',
            'status',
            'progress_percentage',
            'completion_date',
            'associated_costs',
            'comments',
        ]
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 2}),
            'action_description': forms.Textarea(attrs={'rows': 2}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=RemediationAction.STATUS_CHOICES),
        }


# Risk Radar
class RiskRadarForm(forms.ModelForm):
    class Meta:
        model = RiskRadar
        fields = [
            'related_risk',
            'related_action',
            'description',
            'owner',
            'last_updated',
            'zone',
            'color',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'last_updated': forms.DateInput(attrs={'type': 'date'}),
            'zone': forms.Select(choices=RiskRadar.ZONE_CHOICES),
            'color': forms.Select(choices=RiskRadar.COLOR_CHOICES),
        }
 """
