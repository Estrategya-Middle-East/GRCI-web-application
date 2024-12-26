from django import forms
from django.core.exceptions import ValidationError
from .models import *
import json
from django.forms.widgets import DateInput

# 1. Audit Planning Form
class AuditPlanningForm(forms.ModelForm):
    class Meta:
        model = AuditPlanning
        fields = [
            'audit_year',
            'risk_assessment_summary',
            'planned_audits',
            'allocated_resources',
            'approval_status',
            'approval_date',
            'reviewer_id',
            'key_risks',
            'audit_frequency',
            'comments'
        ]
        widgets = {
            'risk_assessment_summary': forms.Textarea(attrs={'rows': 3}),
            'planned_audits': forms.Textarea(attrs={'rows': 3}),
            'allocated_resources': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'key_risks': forms.Textarea(attrs={'rows': 3}),
            'approval_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 2. Audit Universe Register Form
class AuditUniverseRegisterForm(forms.ModelForm):
    class Meta:
        model = AuditUniverseRegister
        fields = [
            'entity_name',
            'risk_score',
            'control_effectiveness',
            'audit_frequency',
            'last_audit_date',
            'next_audit_date',
            'risk_owner',
            'audit_cycle_status',
            'comments'
        ]
        widgets = {
            'control_effectiveness': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'last_audit_date': forms.DateInput(attrs={'type': 'date'}),
            'next_audit_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 3. Risk Mapping Form
class RiskMappingForm(forms.ModelForm):
    class Meta:
        model = RiskMapping
        fields = [
            'process_name',
            'mapped_risks',
            'linked_controls',
            'owner_id',
            'reviewed_date',
            'update_frequency',
            'risk_severity',
            'control_effectiveness',
            'documentation_links',
            'comments'
        ]
        widgets = {
            'mapped_risks': forms.Textarea(attrs={'rows': 3}),
            'linked_controls': forms.Textarea(attrs={'rows': 3}),
            'control_effectiveness': forms.Textarea(attrs={'rows': 3}),
            'documentation_links': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'reviewed_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 4. Engagement Planning Form
class EngagementPlanningForm(forms.ModelForm):
    class Meta:
        model = EngagementPlanning
        fields = [
            'scope',
            'objectives',
            'planned_start_date',
            'planned_end_date',
            'assigned_auditors',
            'risk_focus_areas',
            'approval_status',
            'budget_allocated',
            'milestones',
            'notes'
        ]
        widgets = {
            'scope': forms.Textarea(attrs={'rows': 3}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'risk_focus_areas': forms.Textarea(attrs={'rows': 3}),
            'milestones': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'planned_start_date': forms.DateInput(attrs={'type': 'date'}),
            'planned_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 5. Audit Resource Planner Form
class AuditResourcePlannerForm(forms.ModelForm):
    class Meta:
        model = AuditResourcePlanner
        fields = [
            'team_member',
            'assigned_tasks',
            'availability_status',
            'skillset',
            'allocation_date',
            'engagement_id',
            'hours_allocated',
            'remaining_capacity',
            'comments'
        ]
        widgets = {
            'assigned_tasks': forms.Textarea(attrs={'rows': 3}),
            'skillset': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'allocation_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 6. Execution Log Form
class ExecutionLogForm(forms.ModelForm):
    class Meta:
        model = ExecutionLog
        fields = [
            'engagement_id',
            'audit_criteria',
            'collected_evidence',
            'findings_summary',
            'exceptions',
            'root_cause_analysis',
            'status',
            'completion_date',
            'follow_up_required',
            'recommendations'
        ]
        widgets = {
            'audit_criteria': forms.Textarea(attrs={'rows': 3}),
            'collected_evidence': forms.Textarea(attrs={'rows': 3}),
            'findings_summary': forms.Textarea(attrs={'rows': 3}),
            'exceptions': forms.Textarea(attrs={'rows': 3}),
            'root_cause_analysis': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 7. Follow-Up Form
class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            'audit_id',
            'recommendation',
            'action_plan',
            'assigned_to',
            'due_date',
            'completion_status',
            'review_date',
            'effectiveness_rating',
            'reviewer_comments',
            #'supporting_documents'
        ]
        widgets = {
            'recommendation': forms.Textarea(attrs={'rows': 3}),
            'action_plan': forms.Textarea(attrs={'rows': 3}),
            'reviewer_comments': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 8. Audit Report Form
class AuditReportForm(forms.ModelForm):
    class Meta:
        model = AuditReport
        fields = [
            'audit_id',
            'report_title',
            'findings_summary',
            'recommendations',
            'stakeholder_distribution',
            'report_date',
            'created_by',
            'key_metrics',
            'follow_up_plan',
            #'attached_files'
        ]
        widgets = {
            'findings_summary': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
            'stakeholder_distribution': forms.Textarea(attrs={'rows': 3}),
            'key_metrics': forms.Textarea(attrs={'rows': 3}),
            'follow_up_plan': forms.Textarea(attrs={'rows': 3}),
            'report_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 9. Risk Trends Report Form
class RiskTrendsReportForm(forms.ModelForm):
    class Meta:
        model = RiskTrendsReport
        fields = [
            'recurring_issues',
            'root_causes',
            'impact_level',
            'recommendations',
            'metrics',
            'associated_audits',
            'trend_analysis_date',
            'improvement_plan',
            'owner'
        ]
        widgets = {
            'recurring_issues': forms.Textarea(attrs={'rows': 3}),
            'root_causes': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
            'metrics': forms.Textarea(attrs={'rows': 3}),
            'associated_audits': forms.Textarea(attrs={'rows': 3}),
            'improvement_plan': forms.Textarea(attrs={'rows': 3}),
            'trend_analysis_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 10. Quality Assurance Form
class QualityAssuranceForm(forms.ModelForm):
    class Meta:
        model = QualityAssurance
        fields = [
            'assessment_type',
            'audit_id',
            'compliance_status',
            'improvement_opportunities',
            'reviewer_id',
            'assessment_date',
            'action_plan',
            'implementation_status',
            'follow_up_date',
            'review_summary'
        ]
        widgets = {
            'improvement_opportunities': forms.Textarea(attrs={'rows': 3}),
            'action_plan': forms.Textarea(attrs={'rows': 3}),
            'review_summary': forms.Textarea(attrs={'rows': 3}),
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 11. Fraud Investigation Log Form
class FraudInvestigationLogForm(forms.ModelForm):
    class Meta:
        model = FraudInvestigationLog
        fields = [
            'suspected_fraud_type',
            'details',
            'reported_by',
            'evidence_collected',
            'root_cause',
            'corrective_actions',
            'status',
            'resolution_date',
            'comments',
            #'supporting_files'
        ]
        widgets = {
            'details': forms.Textarea(attrs={'rows': 3}),
            'evidence_collected': forms.Textarea(attrs={'rows': 3}),
            'root_cause': forms.Textarea(attrs={'rows': 3}),
            'corrective_actions': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'resolution_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 12. Document Management Form
class DocumentManagementForm(forms.ModelForm):
    class Meta:
        model = DocumentManagement
        fields = [
            'audit_id',
            'document_title',
            'uploaded_by',
            'upload_date',
            'version',
            'access_permissions',
            'associated_risks',
            'tags',
            'last_updated',
            'file_link'
        ]
        widgets = {
            'access_permissions': forms.Textarea(attrs={'rows': 3}),
            'associated_risks': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.Textarea(attrs={'rows': 3}),
            'upload_date': forms.DateInput(attrs={'type': 'date'}),
            'last_updated': forms.DateInput(attrs={'type': 'date'}),
        }

# 13. Compliance Tracker Form
class ComplianceTrackerForm(forms.ModelForm):
    class Meta:
        model = ComplianceTracker
        fields = [
            'audit_finding',
            'regulation_reference',
            'compliance_status',
            'corrective_actions',
            'follow_up_date',
            'assigned_owner',
            'review_frequency',
            'last_review_date',
            'compliance_rating',
            'comments'
        ]
        widgets = {
            'audit_finding': forms.Textarea(attrs={'rows': 3}),
            'regulation_reference': forms.Textarea(attrs={'rows': 3}),
            'corrective_actions': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'last_review_date': forms.DateInput(attrs={'type': 'date'}),
        }
