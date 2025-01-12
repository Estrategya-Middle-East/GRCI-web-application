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

    path('micro_planning/risk_control_matrix/', views.process_overview, name='risk_control_matrix'),
    path('micro_planning/risk_control_matrix/export/', views.export_process_overview_to_excel, name='export_process_overview_to_excel'),
    # Process
    path('micro_planning/process_understandings/', views.list_process_understanding, name='list_process_understanding'),
    path('micro_planning/process_understandings/add/', views.add_process_understanding, name='add_process_understanding'),
    path('micro_planning/process_understandings/<int:id>/edit/', views.edit_process_understanding, name='edit_process_understanding'),
    path('micro_planning/process_understandings/<int:id>/delete/', views.delete_process_understanding, name='delete_process_understanding'),
   
    # SubProcess
    path('micro_planning/sub_processs/', views.list_sub_process, name='list_sub_process'),
    path('micro_planning/sub_processs/add/', views.add_sub_process, name='add_sub_process'),
    path('micro_planning/sub_processs/<int:id>/edit/', views.edit_sub_process, name='edit_sub_process'),
    path('micro_planning/sub_processs/<int:id>/delete/', views.delete_sub_process, name='delete_sub_process'),

    # Activity
    path('micro_planning/activitys/', views.list_activity, name='list_activity'),
    path('micro_planning/activitys/add/', views.add_activity, name='add_activity'),
    path('micro_planning/activitys/<int:id>/edit/', views.edit_activity, name='edit_activity'),
    path('micro_planning/activitys/<int:id>/delete/', views.delete_activity, name='delete_activity'),

    # Process Risk
    path('micro_planning/process_risks/', views.list_process_risk, name='list_process_risk'),
    path('micro_planning/process_risks/add/', views.add_process_risk, name='add_process_risk'),
    path('micro_planning/process_risks/<int:id>/edit/', views.edit_process_risk, name='edit_process_risk'),
    path('micro_planning/process_risks/<int:id>/delete/', views.delete_process_risk, name='delete_process_risk'),

    # Control
    path('micro_planning/controls/', views.list_control, name='list_control'),
    path('micro_planning/controls/add/', views.add_control, name='add_control'),
    path('micro_planning/controls/<int:id>/edit/', views.edit_control, name='edit_control'),
    path('micro_planning/controls/<int:id>/delete/', views.delete_control, name='delete_control'),

    path('micro_planning/audit_program/', views.audit_program_overview, name='audit_program'),
    path('micro_planning/audit_program/export/', views.export_audit_program_overview_to_excel, name='audit_program_overview_to_excel'),
    # Audit Test
    path('micro_planning/audit_tests/', views.list_audit_test, name='list_audit_test'),
    path('micro_planning/audit_tests/add/', views.add_audit_test, name='add_audit_test'),
    path('micro_planning/audit_tests/<int:id>/edit/', views.edit_audit_test, name='edit_audit_test'),
    path('micro_planning/audit_tests/<int:id>/delete/', views.delete_audit_test, name='delete_audit_test'),

    # Audit Procedure
    path('micro_planning/audit_procedures/', views.list_audit_procedure, name='list_audit_procedure'),
    path('micro_planning/audit_procedures/add/', views.add_audit_procedure, name='add_audit_procedure'),
    path('micro_planning/audit_procedures/<int:id>/edit/', views.edit_audit_procedure, name='edit_audit_procedure'),
    path('micro_planning/audit_procedures/<int:id>/delete/', views.delete_audit_procedure, name='delete_audit_procedure'),

    # Requirements List
    path('micro_planning/requirements_lists/', views.list_requirements_list, name='list_requirements_list'),
    path('micro_planning/requirements_lists/add/', views.add_requirements_list, name='add_requirements_list'),
    path('micro_planning/requirements_lists/<int:id>/edit/', views.edit_requirements_list, name='edit_requirements_list'),
    path('micro_planning/requirements_lists/<int:id>/delete/', views.delete_requirements_list, name='delete_requirements_list'),

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

    #  Draft Report
    path('audit_reporting/draft_reports/', views.list_draft_report, name='list_draft_report'),
    path('audit_reporting/draft_reports/add/', views.add_draft_report, name='add_draft_report'),
    path('audit_reporting/draft_reports/<int:report_id>/edit/', views.edit_draft_report, name='edit_draft_report'),
    path('audit_reporting/draft_reports/<int:report_id>/delete/', views.delete_draft_report, name='delete_draft_report'),

    # Final Report
    path('audit_reporting/final_reports/', views.list_final_report, name='list_final_report'),
    path('audit_reporting/final_reports/add/', views.add_final_report, name='add_final_report'),
    path('audit_reporting/final_reports/<int:report_id>/edit/', views.edit_final_report, name='edit_final_report'),
    path('audit_reporting/final_reports/<int:report_id>/delete/', views.delete_final_report, name='delete_final_report'),

    # Feedback
    path('feedbacks/', views.list_feedback, name='list_feedback'),
    path('feedbacks/add/', views.add_feedback, name='add_feedback'),
    path('feedbacks/<int:survey_id>/edit/', views.edit_feedback, name='edit_feedback'),
    path('feedbacks/<int:survey_id>/delete/', views.delete_feedback, name='delete_feedback'),

    # Follow Up
    path('follow_ups/', views.list_follow_up, name='list_follow_up'),
    path('follow_ups/add/', views.add_follow_up, name='add_follow_up'),
    path('follow_ups/<int:follow_up_id>/edit/', views.edit_follow_up, name='edit_follow_up'),
    path('follow_ups/<int:follow_up_id>/delete/', views.delete_follow_up, name='delete_follow_up'),

 
]

