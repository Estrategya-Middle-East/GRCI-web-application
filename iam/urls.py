"""
URL configuration for GRCi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="iam_dashboard"),  # Default dashboard for IAM
    path("macro_planning/", views.macro_planning_dashboard, name="macro_planning_dashboard"),  # Default dashboard 
    path("micro_planning/", views.micro_planning_dashboard, name="micro_planning_dashboard"),  # Default dashboard
    #path("audit_reporting/", views.audit_reporting_dashboard, name="audit_reporting_dashboard"),  # Default dashboard
    
    # Audit Plan
    path('macro_planning/audit_plans/', views.list_audit_plan, name='list_audit_plan'),
    path('macro_planning/audit_plans/add/', views.add_audit_plan, name='add_audit_plan'),
    path('macro_planning/audit_plans/<int:plan_id>/edit/', views.edit_audit_plan, name='edit_audit_plan'),
    path('macro_planning/audit_plans/<int:plan_id>/delete/', views.delete_audit_plan, name='delete_audit_plan'),

    #AuditUniverseRegister
    path('macro_planning/audit_registers/', views.list_audit_register, name='list_audit_register'),
    path('macro_planning/audit_registers/add/', views.add_audit_register, name='add_audit_register'),
    path('macro_planning/audit_registers/<int:audit_id>/edit/', views.edit_audit_register, name='edit_audit_register'),
    path('macro_planning/audit_registers/<int:audit_id>/delete/', views.delete_audit_register, name='delete_audit_register'),

    #Risk Mapping
    path('macro_planning/risk_assessments/', views.list_risk_assessment, name='list_risk_assessment'),
    path('macro_planning/risk_assessments/add/', views.add_risk_assessment, name='add_risk_assessment'),
    path('macro_planning/risk_assessments/<int:risk_id>/edit/', views.edit_risk_assessment, name='edit_risk_assessment'),
    path('macro_planning/risk_assessments/<int:risk_id>/delete/', views.delete_risk_assessment, name='delete_risk_assessment'),

    # Audit Assessment
    path('micro_planning/audit_assessments/', views.list_audit_assessment, name='list_audit_assessment'),
    path('micro_planning/audit_assessments/add/', views.add_audit_assessment, name='add_audit_assessment'),
    path('micro_planning/audit_assessments/<int:assessment_id>/edit/', views.edit_audit_assessment, name='edit_audit_assessment'),
    path('micro_planning/audit_assessments/<int:assessment_id>/delete/', views.delete_audit_assessment, name='delete_audit_assessment'),

    # Audit Notification
    path('micro_planning/audit_notifications/', views.list_audit_notification, name='list_audit_notification'),
    path('micro_planning/audit_notifications/add/', views.add_audit_notification, name='add_audit_notification'),
    path('micro_planning/audit_notifications/<int:notification_id>/edit/', views.edit_audit_notification, name='edit_audit_notification'),
    path('micro_planning/audit_notifications/<int:notification_id>/delete/', views.delete_audit_notification, name='delete_audit_notification'),

    # Entrance Meeting
    path('micro_planning/entrance_meetings/', views.list_entrance_meeting, name='list_entrance_meeting'),
    path('micro_planning/entrance_meetings/add/', views.add_entrance_meeting, name='add_entrance_meeting'),
    path('micro_planning/entrance_meetings/<int:meeting_id>/edit/', views.edit_entrance_meeting, name='edit_entrance_meeting'),
    path('micro_planning/entrance_meetings/<int:meeting_id>/delete/', views.delete_entrance_meeting, name='delete_entrance_meeting'),

    # Sub-Process Risk Assessment
    path('micro_planning/sub_risk_assessments/', views.list_sub_risk_assessment, name='list_sub_risk_assessment'),
    path('micro_planning/sub_risk_assessments/add/', views.add_sub_risk_assessment, name='add_sub_risk_assessment'),
    path('micro_planning/sub_risk_assessments/<int:assessment_id>/edit/', views.edit_sub_risk_assessment, name='edit_sub_risk_assessment'),
    path('micro_planning/sub_risk_assessments/<int:assessment_id>/delete/', views.delete_sub_risk_assessment, name='delete_sub_risk_assessment'),

    # Audit Program
    path('micro_planning/audit_programs/', views.list_audit_program, name='list_audit_program'),
    path('micro_planning/audit_programs/add/', views.add_audit_program, name='add_audit_program'),
    path('micro_planning/audit_programs/<int:program_id>/edit/', views.edit_audit_program, name='edit_audit_program'),
    path('micro_planning/audit_programs/<int:program_id>/delete/', views.delete_audit_program, name='delete_audit_program'),

    # Working Paper
    path('fieldwork/working_papers/', views.list_working_paper, name='list_working_paper'),
    path('fieldwork/working_papers/add/', views.add_working_paper, name='add_working_paper'),
    path('fieldwork/working_papers/<int:working_paper_id>/edit/', views.edit_working_paper, name='edit_working_paper'),
    path('fieldwork/working_papers/<int:working_paper_id>/delete/', views.delete_working_paper, name='delete_working_paper'),

    # Observation Sheet
    path('fieldwork/observation_sheets/', views.list_observation_sheet, name='list_observation_sheet'),
    path('fieldwork/observation_sheets/add/', views.add_observation_sheet, name='add_observation_sheet'),
    path('fieldwork/observation_sheets/<int:observation_id>/edit/', views.edit_observation_sheet, name='edit_observation_sheet'),
    path('fieldwork/observation_sheets/<int:observation_id>/delete/', views.delete_observation_sheet, name='delete_observation_sheet'),
 
    # Observation Sheet
    path('fieldwork/other_notess/', views.list_other_notes, name='list_other_notes'),
    path('fieldwork/other_notess/add/', views.add_other_notes, name='add_other_notes'),
    path('fieldwork/other_notess/<int:note_id>/edit/', views.edit_other_notes, name='edit_other_notes'),
    path('fieldwork/other_notess/<int:note_id>/delete/', views.delete_other_notes, name='delete_other_notes'),

    # Entrance Meeting
    path('audit_reporting/exit_meetings/', views.list_exit_meeting, name='list_exit_meeting'),
    path('audit_reporting/exit_meetings/add/', views.add_exit_meeting, name='add_exit_meeting'),
    path('audit_reporting/exit_meetings/<int:meeting_id>/edit/', views.edit_exit_meeting, name='edit_exit_meeting'),
    path('audit_reporting/exit_meetings/<int:meeting_id>/delete/', views.delete_exit_meeting, name='delete_exit_meeting'),
  
]


""" 

    # Quality Assurance
    path('quality_assurances/', views.list_quality_assurance, name='list_quality_assurance'),
    path('quality_assurances/add/', views.add_quality_assurance, name='add_quality_assurance'),
    path('quality_assurances/<int:qa_id>/edit/', views.edit_quality_assurance, name='edit_quality_assurance'),
    path('quality_assurances/<int:qa_id>/delete/', views.delete_quality_assurance, name='delete_quality_assurance'),

    # Fraud Investigation
    path('fraud_investigations/', views.list_fraud_investigation, name='list_fraud_investigation'),
    path('fraud_investigations/add/', views.add_fraud_investigation, name='add_fraud_investigation'),
    path('fraud_investigations/<int:investigation_id>/edit/', views.edit_fraud_investigation, name='edit_fraud_investigation'),
    path('fraud_investigations/<int:investigation_id>/delete/', views.delete_fraud_investigation, name='delete_fraud_investigation'),

    # Compliance Tracker
    path('compliance_trackers/', views.list_compliance_tracker, name='list_compliance_tracker'),
    path('compliance_trackers/add/', views.add_compliance_tracker, name='add_compliance_tracker'),
    path('compliance_trackers/<int:compliance_id>/edit/', views.edit_compliance_tracker, name='edit_compliance_tracker'),
    path('compliance_trackers/<int:compliance_id>/delete/', views.delete_compliance_tracker, name='delete_compliance_tracker'),

"""