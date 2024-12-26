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
    path("audit_oversight/", views.audit_oversight_dashboard, name="audit_oversight_dashboard"),  # Default dashboard 
    path("audit_engagement/", views.audit_engagement_dashboard, name="audit_engagement_dashboard"),  # Default dashboard
    path("audit_reporting/", views.audit_reporting_dashboard, name="audit_reporting_dashboard"),  # Default dashboard
    
    # Audit Planning
    path('audit_oversight/audit_plannings/', views.list_audit_planning, name='list_audit_planning'),
    path('audit_oversight/audit_plannings/add/', views.add_audit_planning, name='add_audit_planning'),
    path('audit_oversight/audit_plannings/<int:plan_id>/edit/', views.edit_audit_planning, name='edit_audit_planning'),
    path('audit_oversight/audit_plannings/<int:plan_id>/delete/', views.delete_audit_planning, name='delete_audit_planning'),

    #AuditUniverseRegister
    path('audit_oversight/audit_registers/', views.list_audit_register, name='list_audit_register'),
    path('audit_oversight/audit_registers/add/', views.add_audit_register, name='add_audit_register'),
    path('audit_oversight/audit_registers/<int:entity_id>/edit/', views.edit_audit_register, name='edit_audit_register'),
    path('audit_oversight/audit_registers/<int:entity_id>/delete/', views.delete_audit_register, name='delete_audit_register'),

    #Risk Mapping
    path('risk_mappings/', views.list_risk_mapping, name='list_risk_mapping'),
    path('risk_mappings/add/', views.add_risk_mapping, name='add_risk_mapping'),
    path('risk_mappings/<int:process_id>/edit/', views.edit_risk_mapping, name='edit_risk_mapping'),
    path('risk_mappings/<int:process_id>/delete/', views.delete_risk_mapping, name='delete_risk_mapping'),

    # Audit Engagement
    path('audit_engagement/engagement_plannings/', views.list_engagement_planning, name='list_engagement_planning'),
    path('audit_engagement/engagement_plannings/add/', views.add_engagement_planning, name='add_engagement_planning'),
    path('audit_engagement/engagement_plannings/<int:engagement_id>/edit/', views.edit_engagement_planning, name='edit_engagement_planning'),
    path('audit_engagement/engagement_plannings/<int:engagement_id>/delete/', views.delete_engagement_planning, name='delete_engagement_planning'),

    #Audit Resource
    path('audit_engagement/audit_resources/', views.list_audit_resource, name='list_audit_resource'),
    path('audit_engagement/audit_resources/add/', views.add_audit_resource, name='add_audit_resource'),
    path('audit_engagement/audit_resources/<int:resource_id>/edit/', views.edit_audit_resource, name='edit_audit_resource'),
    path('audit_engagement/audit_resources/<int:resource_id>/delete/', views.delete_audit_resource, name='delete_audit_resource'),

    # Audit Execution
    path('audit_executions/', views.list_audit_execution, name='list_audit_execution'),
    path('audit_executions/add/', views.add_audit_execution, name='add_audit_execution'),
    path('audit_executions/<int:execution_id>/edit/', views.edit_audit_execution, name='edit_audit_execution'),
    path('audit_executions/<int:execution_id>/delete/', views.delete_audit_execution, name='delete_audit_execution'),

    # FollowUp
    path('follow_ups/', views.list_follow_up, name='list_follow_up'),
    path('follow_ups/add/', views.add_follow_up, name='add_follow_up'),
    path('follow_ups/<int:follow_up_id>/edit/', views.edit_follow_up, name='edit_follow_up'),
    path('follow_ups/<int:follow_up_id>/delete/', views.delete_follow_up, name='delete_follow_up'),

    # Audit Reporting
    path('audit_reporting/audit_reports/', views.list_audit_report, name='list_audit_report'),
    path('audit_reporting/audit_reports/add/', views.add_audit_report, name='add_audit_report'),
    path('audit_reporting/audit_reports/<int:report_id>/edit/', views.edit_audit_report, name='edit_audit_report'),
    path('audit_reporting/audit_reports/<int:report_id>/delete/', views.delete_audit_report, name='delete_audit_report'),

    # Risk Trends Report
    path('audit_reporting/risktrends_reports/', views.list_risktrends_report, name='list_risktrends_report'),
    path('audit_reporting/risktrends_reports/add/', views.add_risktrends_report, name='add_risktrends_report'),
    path('audit_reporting/risktrends_reports/<int:trend_id>/edit/', views.edit_risktrends_report, name='edit_risktrends_report'),
    path('audit_reporting/risktrends_reports/<int:trend_id>/delete/', views.delete_risktrends_report, name='delete_risktrends_report'),

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

]


