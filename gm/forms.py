from django import forms
from django.core.exceptions import ValidationError
from .models import *
import json
from django.forms import DateInput, Textarea


class GovernanceStructureForm(forms.ModelForm):
    class Meta:
        model = GovernanceStructure
        fields = [
            'charter_name',
            'approver_id',
            'roles_and_responsibilities',
            'approval_status',
            'approval_date',
            'review_frequency',
            'stewardship_owner',
            #'supporting_documents',
            'review_date',
            'comments',
        ]
        widgets = {
            'roles_and_responsibilities': Textarea(attrs={'rows': 2}),
            'approval_date': DateInput(attrs={'type': 'date'}),
            'review_date': DateInput(attrs={'type': 'date'}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class LeadershipAccountabilityForm(forms.ModelForm):
    class Meta:
        model = LeadershipAccountability
        fields = [
            'role_name',
            'responsibilities',
            'accountable_to',
            'decision_authority',
            'approval_status',
            'review_date',
            'role_owner',
            'key_metrics',
            'improvement_areas',
            'comments',
        ]
        widgets = {
            'responsibilities': Textarea(attrs={'rows': 2}),
            'decision_authority': Textarea(attrs={'rows': 2}),
            'review_date': DateInput(attrs={'type': 'date'}),
            'key_metrics': Textarea(attrs={'rows': 2}),
            'improvement_areas': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class PurposeAndValuesForm(forms.ModelForm):
    class Meta:
        model = PurposeAndValues
        fields = [
            'purpose_statement',
            'core_values',
            'ethical_principles',
            'approved_by',
            'approval_date',
            'stakeholder_feedback',
            'review_frequency',
            'stewardship_owner',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'purpose_statement': Textarea(attrs={'rows': 2}),
            'core_values': Textarea(attrs={'rows': 2}),
            'ethical_principles': Textarea(attrs={'rows': 2}),
            'approval_date': DateInput(attrs={'type': 'date'}),
            'stakeholder_feedback': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class StrategicDirectionForm(forms.ModelForm):
    class Meta:
        model = StrategicDirection
        fields = [
            'objective',
            'strategic_alignment',
            'kpi',
            'owner',
            'resources_allocated',
            'review_frequency',
            'last_review_date',
            'approval_status',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'objective': Textarea(attrs={'rows': 2}),
            'strategic_alignment': Textarea(attrs={'rows': 2}),
            'kpi': Textarea(attrs={'rows': 2}),
            'last_review_date': DateInput(attrs={'type': 'date'}),
            'resources_allocated': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class ResourceManagementForm(forms.ModelForm):
    class Meta:
        model = ResourceManagement
        fields = [
            'resource_type',
            'allocated_to',
            'allocation_date',
            'risk_assessment',
            'owner',
            'utilization_metrics',
            'compliance_status',
            'last_audit_date',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'allocation_date': DateInput(attrs={'type': 'date'}),
            'risk_assessment': Textarea(attrs={'rows': 2}),
            'utilization_metrics': Textarea(attrs={'rows': 2}),
            'last_audit_date': DateInput(attrs={'type': 'date'}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class RiskAndComplianceForm(forms.ModelForm):
    class Meta:
        model = RiskAndCompliance
        fields = [
            'risk_name',
            'risk_severity',
            'regulatory_requirement',
            'compliance_status',
            'owner',
            'last_review_date',
            'improvement_actions',
            #'supporting_documents',
            'review_frequency',
            'comments',
        ]
        widgets = {
            'regulatory_requirement': Textarea(attrs={'rows': 2}),
            'last_review_date': DateInput(attrs={'type': 'date'}),
            'improvement_actions': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class PerformanceReportingForm(forms.ModelForm):
    class Meta:
        model = PerformanceReporting
        fields = [
            'report_type',
            'reporting_period',
            'kpis_assessed',
            'performance_summary',
            'prepared_by',
            'approved_by',
            'distribution_list',
            'review_frequency',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'reporting_period': Textarea(attrs={'rows': 2}),
            'kpis_assessed': Textarea(attrs={'rows': 2}),
            'performance_summary': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
            'distribution_list': Textarea(attrs={'rows': 2}),
        }

class StakeholderEngagementForm(forms.ModelForm):
    class Meta:
        model = StakeholderEngagement
        fields = [
            'stakeholder_group',
            'engagement_type',
            'feedback_collected',
            'action_taken',
            'communication_date',
            'owner',
            'key_issues',
            'resolution_status',
           #'supporting_documents',
            'comments',
        ]
        widgets = {
            'engagement_type': Textarea(attrs={'rows': 2}),
            'feedback_collected': Textarea(attrs={'rows': 2}),
            'action_taken': Textarea(attrs={'rows': 2}),
            'communication_date': DateInput(attrs={'type': 'date'}),
            'key_issues': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class EthicalGovernanceForm(forms.ModelForm):
    class Meta:
        model = EthicalGovernance
        fields = [
            'code_of_conduct_reference',
            'incident_type',
            'incident_reported_by',
            'resolution_status',
            'responsible_owner',
            'follow_up_actions',
            'review_date',
           #'supporting_documents',
            'comments',
            'ethical_risk_rating',
        ]
        widgets = {
            'code_of_conduct_reference': Textarea(attrs={'rows': 2}),
            'follow_up_actions': Textarea(attrs={'rows': 2}),
            'review_date': DateInput(attrs={'type': 'date'}),
            'comments': Textarea(attrs={'rows': 2}),
            'ethical_risk_rating': Textarea(attrs={'rows': 2}),
        }

class GovernanceImprovementForm(forms.ModelForm):
    class Meta:
        model = GovernanceImprovement
        fields = [
            'initiative_name',
            'improvement_objective',
            'owner',
            'start_date',
            'target_completion_date',
            'progress_status',
            'resources_allocated',
            'impact_assessment',
           #'supporting_documents',
            'comments',
        ]
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'target_completion_date': DateInput(attrs={'type': 'date'}),
            'improvement_objective': Textarea(attrs={'rows': 2}),
            'resources_allocated': Textarea(attrs={'rows': 2}),
            'impact_assessment': Textarea(attrs={'rows': 2}),
            'comments': Textarea(attrs={'rows': 2}),
        }

class GovernanceDocumentManagementForm(forms.ModelForm):
    class Meta:
        model = GovernanceDocumentManagement
        fields= '__all__'
        exclude = ['document_id']
        widgets = {
            'upload_date': DateInput(attrs={'type': 'date'}),
            'associated_processes': Textarea(attrs={'rows': 2}),
            'tags': Textarea(attrs={'rows': 2}),
        }