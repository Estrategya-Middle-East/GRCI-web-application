from django import forms
from django.core.exceptions import ValidationError
from .models import *
import json
from django.forms.widgets import DateInput


 
# Macro Planning (Annual) #

# 1. Audit Universe
class AuditUniverseForm(forms.ModelForm):
    class Meta:
        model = AuditUniverse
        fields = [    
            'entity_name',
            'risk_category',
            'priority_level',
            'last_audit_date',
            'next_audit_date',
            'assigned_auditor', 
            'comments',]
            
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'last_audit_date': forms.DateInput(attrs={'type': 'date'}),
            'next_audit_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
# 2. Risk Assessment
class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = [
            'entity_name',
            'risk_type',
            'inherent_risk',
            'residual_risk',
            'control_effectiveness',
            'assessed_by',
            'assessed_date',
            'risk_severity',
            'comments'
            ]
        
        widgets = {
        'comments': forms.Textarea(attrs={'rows': 3}),
        'control_effectiveness': forms.Textarea(attrs={'rows': 3}),
        'assessed_date': forms.DateInput(attrs={'type': 'date'}),
        }  

    

# 3. Annual Audit Plan (AAP)
class AuditPlanForm(forms.ModelForm):
    class Meta:
        model = AuditPlan
        fields = [

            'audit_year',
            'entity_name',
            'audit_frequency',
            'priority_level',
            'allocated_resources',
            'audit_schedule',
            'assigned_team',
            'comments']

        widgets = {
            'allocated_resources': forms.Textarea(attrs={'rows': 3}),
            'audit_schedule': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            }

# Macro Planning (Annual) #

# 4. Audit Assessment
class AuditAssessmentForm(forms.ModelForm):
    class Meta:
        model = AuditAssessment
        fields = [
            'entity_name',
            'assigned_team', 
            'scope',
            'objectives',
            'start_date',
            'end_date',
            'comments',]
    
        widgets = {
            'scope': forms.Textarea(attrs={'rows': 3}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


# 5. Audit Notification
class AuditNotificationForm(forms.ModelForm):
    class Meta:
        model = AuditNotification
        fields = [
            'entity_name',
            'auditee_name',
            'audit_scope',
            'objectives',
            'audit_timeline',
            'notification_date',
            'comments',]

        widgets = {
            'audit_scope': forms.Textarea(attrs={'rows': 3}),
            'objectives': forms.Textarea(attrs={'rows': 3}),
            'audit_timeline': forms.Textarea(attrs={'rows': 3}),
            'notification_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
    
# 6. Entrance Meeting
class EntranceMeetingForm(forms.ModelForm):
    class Meta:
        model = EntranceMeeting
        fields = [
            'entity_name',
            'participants',
            'discussion_points',
            'meeting_date',
            'comments']

        widgets = {
            'discussion_points': forms.Textarea(attrs={'rows': 3}),
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


# 7. Sub-Process Risk Assessment (ORC)	
class SubRiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = SubRiskAssessment
        fields = [
                    'sub_process_name',
                    'entity_name',
                    'risk_category',
                    'inherent_risk',
                    'residual_risk',
                    'control_effectiveness',
                    'assessed_by',
                    'assessed_date',
                    'risk_severity',
                    'comments',]
            
        widgets = {
            'control_effectiveness': forms.Textarea(attrs={'rows': 3}),
            'comments': forms.Textarea(attrs={'rows': 3}),
            'assessed_date': forms.DateInput(attrs={'type': 'date'}),
        }
   

# 8. Audit Program
class AuditProgramForm(forms.ModelForm):
    class Meta:
        model = AuditProgram
        fields = [
            'entity_name',
            'sub_process_name',
            'procedures',
            'tests',
            'assigned_auditors',
            'program_date',
            'comments']
    
        widgets = {
        'comments': forms.Textarea(attrs={'rows': 3}),
        'procedures': forms.Textarea(attrs={'rows': 3}),
        'tests': forms.Textarea(attrs={'rows': 3}),
        'program_date': forms.DateInput(attrs={'type': 'date'}),
        }


# Fieldwork (Per Audit) #

# 9. Working Paper
class WorkingPaperForm(forms.ModelForm):
    class Meta:
        model = WorkingPaper
        fields = [  
            'entity_name',
            'audit_task',
            'evidence_collected',
            'performed_by',
            'task_completion_date',
            'comments',]
    
        widgets = {
            'evidence_collected': forms.Textarea(attrs={'rows': 3}),
            'task_completion_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

# 10. Observation Sheet
class ObservationSheetForm(forms.ModelForm):
    class Meta:
        model = ObservationSheet
        fields = [
            'entity_name',
            'observation_details',
            'impact',
            'recommendation',
            'assigned_to',
            'deadline',
            'comments']

        widgets = {
            'observation_details': forms.Textarea(attrs={'rows': 3}),
            'impact': forms.Textarea(attrs={'rows': 3}),
            'recommendation': forms.Textarea(attrs={'rows': 3}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
    
# 11. Other Notes
class OtherNotesForm(forms.ModelForm):
    class Meta:
        model = OtherNotes
        fields = [  
            'entity_name',
            'note_details',
            'added_by',
            'note_date',
            'comments']

        widgets = {
            'note_details': forms.Textarea(attrs={'rows': 3}),
            'note_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


# Reporting (Per Audit) #

# 12. Draft Report
class DraftReportForm(forms.ModelForm):
    class Meta:
        model = DraftReport
        fields = [
            'entity_name',
            'findings',
            'recommendations',
            'drafted_by',
            'draft_date',
            'comments']

        widgets = {
            'findings': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
            'draft_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

# 13. Exit Meeting
class ExitMeetingForm(forms.ModelForm):
    class Meta:
        model = ExitMeeting
        fields = [
            'entity_name',
            'participants', 
            'discussion_points',
            'agreed_actions',
            'meeting_date',
            'comments',]

        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'discussion_points': forms.Textarea(attrs={'rows': 3}),
            'agreed_actions': forms.Textarea(attrs={'rows': 3}),
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

# 14. Final Report
class FinalReportForm(forms.ModelForm):
    class Meta:
        model = FinalReport
        fields = [
            'entity_name',
            'findings_summary',
            'recommendations',
            'approved_by',
            'submission_date',
            'comments',]
    
        widgets = {
            'findings_summary': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
            'submission_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


# Feedback (Per Audit) #

# 15. Feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'entity_name',
            'auditee_name',
            'feedback_details',
            'survey_date',
            'comments',]

        widgets = {
            'feedback_details': forms.Textarea(attrs={'rows': 3}),
            'survey_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


# Follow-Up (Per Audit) #

# 16. Audit Follow-Up
class AuditFollowUpForm(forms.ModelForm):
    class Meta:
        model = AuditFollowUp
        fields = [
            'entity_name',
            'issues_resolved',
            'corrective_actions',
            'follow_up_by',
            'follow_up_date',
            'comments',]

        widgets = {
            'issues_resolved': forms.Textarea(attrs={'rows': 3}),
            'corrective_actions': forms.Textarea(attrs={'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
    
