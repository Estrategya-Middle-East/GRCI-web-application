from django import forms
from django.core.exceptions import ValidationError
from .models import *
import json
from django.forms.widgets import DateInput


class BCMGovernanceForm(forms.ModelForm):
    class Meta:
        model = BCMGovernance
        fields = [
            'bcm_policy_title',
            'approver_id',
            'roles_and_responsibilities',
            'approval_status',
            'approval_date',
            'review_frequency',
            'governance_owner',
            #'supporting_documents',
            'review_date',
            'comments',
        ]
        widgets = {
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'roles_and_responsibilities': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

class BusinessImpactAnalysisForm(forms.ModelForm):
    class Meta:
        model = BusinessImpactAnalysis
        fields = [
            'business_function',
            'impact_level',
            'dependencies',
            'maximum_tolerable_downtime',
            'recovery_time_objective',
            'critical_resources',
            'review_date',
            'impact_description',
            'reviewed_by',
            'comments',
        ]
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'dependencies': forms.Textarea(attrs={'rows': 2}),
            'critical_resources': forms.Textarea(attrs={'rows': 2}),
            'impact_description': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

class ContinuityRiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = ContinuityRiskAssessment
        fields = [
            'risk_name',
            'impact_likelihood',
            'risk_severity',
            'associated_bcp',
            'mitigation_plan',
            'risk_owner',
            'assessment_date',
            'review_cycle',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            'mitigation_plan': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
            'associated_bcp': forms.Textarea(attrs={'rows': 2}),
        }

class ContinuityStrategyForm(forms.ModelForm):
    class Meta:
        model = ContinuityStrategy
        fields = [
            'strategy_name',
            'recovery_objective',
            'resources_required',
            'third_party_dependencies',
            'associated_business_functions',
            'approval_status',
            'approval_date',
            'reviewer_id',
            'review_frequency',
            'comments',
        ]
        widgets = {
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
            'recovery_objective': forms.Textarea(attrs={'rows': 2}),
            'resources_required': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
            'third_party_dependencies': forms.Textarea(attrs={'rows': 2}),
            'associated_business_functions': forms.Textarea(attrs={'rows': 2}),
        }

class BusinessContinuityPlanForm(forms.ModelForm):
    class Meta:
        model = BusinessContinuityPlan
        fields = [
            'plan_name',
            'business_function',
            'plan_owner',
            'recovery_steps',
            'contact_list',
            'activation_criteria',
            'testing_schedule',
            'last_test_date',
            'approval_status',
            'comments',
        ]
        widgets = {
            'last_test_date': forms.DateInput(attrs={'type': 'date'}),
            'recovery_steps': forms.Textarea(attrs={'rows': 2}),
            'contact_list': forms.Textarea(attrs={'rows': 2}),
            'activation_criteria': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
            'testing_schedule': forms.Textarea(attrs={'rows': 2}),
        }

class ContinuityTestingForm(forms.ModelForm):
    class Meta:
        model = ContinuityTesting
        fields = [
            'test_scenario',
            'test_date',
            'participants',
            'test_results',
            'issues_identified',
            'improvement_plan',
            'follow_up_date',
            'next_scheduled_test',
            'reviewed_by',
            'comments',
        ]
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'next_scheduled_test': forms.DateInput(attrs={'type': 'date'}),
            'test_scenario': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
            'participants': forms.Textarea(attrs={'rows': 2}),
            'test_results': forms.Textarea(attrs={'rows': 2}),
            'issues_identified': forms.Textarea(attrs={'rows': 2}),
            'improvement_plan': forms.Textarea(attrs={'rows': 2}),
        }

class IncidentActivationLogForm(forms.ModelForm):
    class Meta:
        model = IncidentActivationLog
        fields = [
            'incident_type',
            'date_activated',
            'bcp_activated',
            'decision_maker',
            'resources_mobilized',
            'status_updates',
            'closure_date',
            'lessons_learned',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'date_activated': forms.DateInput(attrs={'type': 'date'}),
            'closure_date': forms.DateInput(attrs={'type': 'date'}),
            'resources_mobilized': forms.Textarea(attrs={'rows': 2}),
            'lessons_learned': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
            'status_updates': forms.Textarea(attrs={'rows': 2}),
        }

class CrisisCommunicationForm(forms.ModelForm):
    class Meta:
        model = CrisisCommunication
        fields = [
            'incident_id',
            'recipient_groups',
            'message_template',
            'date_sent',
            'sent_by',
            'acknowledgment_status',
            'follow_up_required',
            'escalation_plan',
            'feedback',
            #'attachments',
        ]
        widgets = {
            'date_sent': forms.DateInput(attrs={'type': 'date'}),
            'message_template': forms.Textarea(attrs={'rows': 2}),
            'feedback': forms.Textarea(attrs={'rows': 2}),
            'recipient_groups': forms.Textarea(attrs={'rows': 2}),
            'escalation_plan': forms.Textarea(attrs={'rows': 2}),
        }

class BCMProgramReviewForm(forms.ModelForm):
    class Meta:
        model = BCMProgramReview
        fields = [
            'program_name',
            'reviewer_id',
            'review_date',
            'key_findings',
            'compliance_status',
            'improvement_recommendations',
            'implementation_plan',
            'follow_up_actions',
            #'supporting_documents',
            'comments',
        ]
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'key_findings': forms.Textarea(attrs={'rows': 2}),
            'improvement_recommendations': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }

class BCMDocumentManagementForm(forms.ModelForm):
    class Meta:
        model = BCMDocumentManagement
        fields = [
            'document_title',
            'uploaded_by',
            'upload_date',
            'version',
            'document_type',
            'associated_plans',
            'tags',
            'access_permissions',
            'last_updated',
            'file_link',
        ]
        widgets = {
            'upload_date': forms.DateInput(attrs={'type': 'date'}),
            'last_updated': forms.DateInput(attrs={'type': 'date'}),
        }
