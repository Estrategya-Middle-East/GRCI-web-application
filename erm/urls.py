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
from .views import RiskWorkflowView

urlpatterns = [
    path("", views.dashboard, name="erm_dashboard"),  # Default dashboard for ERM
    path("leadership/", views.leadership_dashboard, name="leadership_dashboard"),  # Default dashboard for ERM
    path("strategic_planning/", views.strategic_planning_dashboard, name="strategic_planning_dashboard"),  # Default dashboard for ERM
    path("continuous_monitoring/", views.continuous_monitoring_dashboard, name="continuous_monitoring_dashboard"),  # Default dashboard for ERM
    path("risk_intelligence/", views.risk_intelligence_dashboard, name="risk_intelligence_dashboard"),  # Default dashboard for ERM
    
 
    path('export/', views.export_all_to_excel, name='export_all_to_excel'),
    #workflow Risk 
    path('risks/', views.list_risks, name='list_risks'),
    path('export_risks/', views.export_risks_to_excel, name='export_risks'),
    
    path('risks/add/', views.add_risk, name='add_risk'),
    path('risks/<int:id>/edit/', views.edit_risk, name='edit_risk'),
    path('risks/<int:id>/delete/', views.delete_risk, name='delete_risk'),
    path('workflow/<int:id>/', RiskWorkflowView.as_view(), name='workflow_view'),


    #leadership
    path('leadership/board_oversights/', views.list_board_oversight, name='list_board_oversight'),
    path('leadership/board_oversights/add/', views.add_board_oversight, name='add_board_oversight'),
    path('leadership/board_oversights/<int:OversightID>/edit/', views.edit_board_oversight, name='edit_board_oversight'),
    path('leadership/board_oversights/<int:OversightID>/delete/', views.delete_board_oversight, name='delete_board_oversight'),

    #Operating Structures Manager
    path('leadership/operating_structures/', views.list_operating_structure, name='list_operating_structure'),
    path('leadership/operating_structures/add/', views.add_operating_structure, name='add_operating_structure'),
    path('leadership/operating_structures/<int:StructureID>/edit/', views.edit_operating_structure, name='edit_operating_structure'),
    path('leadership/operating_structures/<int:StructureID>/delete/', views.delete_operating_structure, name='delete_operating_structure'),

    #Culture Survey
    path('leadership/culture_surveys/', views.list_culture_survey, name='list_culture_survey'),
    path('leadership/culture_surveys/add/', views.add_culture_survey, name='add_culture_survey'),
    path('leadership/culture_surveys/<int:SurveyID>/edit/', views.edit_culture_survey, name='edit_culture_survey'),
    path('leadership/culture_surveys/<int:SurveyID>/delete/', views.delete_culture_survey, name='delete_culture_survey'),

    #CoreValuesMonitoring
    path('leadership/corevalues_monitorings/', views.list_corevalues_monitoring, name='list_corevalues_monitoring'),
    path('leadership/corevalues_monitorings/add/', views.add_corevalues_monitoring, name='add_corevalues_monitoring'),
    path('leadership/corevalues_monitorings/<int:MonitoringID>/edit/', views.edit_corevalues_monitoring, name='edit_corevalues_monitoring'),
    path('leadership/corevalues_monitorings/<int:MonitoringID>/delete/', views.delete_corevalues_monitoring, name='delete_corevalues_monitoring'),

    #Talent Management for Risk
    path('leadership/talent_managements/', views.list_talent_management, name='list_talent_management'),
    path('leadership/talent_managements/add/', views.add_talent_management, name='add_talent_management'),
    path('leadership/talent_managements/<int:TalentID>/edit/', views.edit_talent_management, name='edit_talent_management'),
    path('leadership/talent_managements/<int:TalentID>/delete/', views.delete_talent_management, name='delete_talent_management'),

    # Strategic Planning
    # Business Context
    path('strategic_planning/business_contexts/', views.list_business_context, name='list_business_context'),
    path('strategic_planning/business_contexts/add/', views.add_business_context, name='add_business_context'),
    path('strategic_planning/business_contexts/<int:context_id>/edit/', views.edit_business_context, name='edit_business_context'),
    path('strategic_planning/business_contexts/<int:context_id>/delete/', views.delete_business_context, name='delete_business_context'),

    # Risk Appetite
    path('strategic_planning/risk_appetites/', views.list_risk_appetite, name='list_risk_appetite'),
    path('strategic_planning/risk_appetites/add/', views.add_risk_appetite, name='add_risk_appetite'),
    path('strategic_planning/risk_appetites/<int:appetite_id>/edit/', views.edit_risk_appetite, name='edit_risk_appetite'),
    path('strategic_planning/risk_appetites/<int:appetite_id>/delete/', views.delete_risk_appetite, name='delete_risk_appetite'),

    # Strategic Evaluation
    path('strategic_planning/strategic_evaluations/', views.list_strategic_evaluation, name='list_strategic_evaluation'),
    path('strategic_planning/strategic_evaluations/add/', views.add_strategic_evaluation, name='add_strategic_evaluation'),
    path('strategic_planning/strategic_evaluations/<int:evaluation_id>/edit/', views.edit_strategic_evaluation, name='edit_strategic_evaluation'),
    path('strategic_planning/strategic_evaluations/<int:evaluation_id>/delete/', views.delete_strategic_evaluation, name='delete_strategic_evaluation'),

    # Objectives
    path('strategic_planning/objectives/', views.list_objective, name='list_objective'),
    path('strategic_planning/objectives/add/', views.add_objective, name='add_objective'),
    path('strategic_planning/objectives/<int:id>/edit/', views.edit_objective, name='edit_objective'),
    path('strategic_planning/objectives/<int:id>/delete/', views.delete_objective, name='delete_objective'),

    # Continuous monitoring
    path('continuous_monitoring/change_assessments/', views.list_change_assessment, name='list_change_assessment'),
    path('continuous_monitoring/change_assessments/add/', views.add_change_assessment, name='add_change_assessment'),
    path('continuous_monitoring/change_assessments/<int:change_id>/edit/', views.edit_change_assessment, name='edit_change_assessment'),
    path('continuous_monitoring/change_assessments/<int:change_id>/delete/', views.delete_change_assessment, name='delete_change_assessment'),

    # Performance Review
    path('continuous_monitoring/performance_reviews/', views.list_performance_review, name='list_performance_review'),
    path('continuous_monitoring/performance_reviews/add/', views.add_performance_review, name='add_performance_review'),
    path('continuous_monitoring/performance_reviews/<int:review_id>/edit/', views.edit_performance_review, name='edit_performance_review'),
    path('continuous_monitoring/performance_reviews/<int:review_id>/delete/', views.delete_performance_review, name='delete_performance_review'),

    # Improvement Action
    path('continuous_monitoring/improvement_actions/', views.list_improvement_action, name='list_improvement_action'),
    path('continuous_monitoring/improvement_actions/add/', views.add_improvement_action, name='add_improvement_action'),
    path('continuous_monitoring/improvement_actions/<int:improvement_id>/edit/', views.edit_improvement_action, name='edit_improvement_action'),
    path('continuous_monitoring/improvement_actions/<int:improvement_id>/delete/', views.delete_improvement_action, name='delete_improvement_action'),

]



"""
   path('objectives/', views.list_objectives, name='list_objectives'),
    path('objectives/add/', views.add_objective, name='add_objective'),
    path('objectives/<int:id>/', views.edit_objective, name='edit_objective'),
    path('objectives/delete/<int:id>/', views.delete_objective, name='delete_objective'),
    
    path('strategies/', views.list_objective_strategies, name='list_objective_strategies'),
    path('strategies/add/', views.add_objective_strategy, name='add_objective_strategy'),
    path('strategies/<int:id>/', views.edit_objective_strategy, name='edit_objective_strategy'),
    path('strategies/delete/<int:id>/', views.delete_objective_strategy, name='delete_objective_strategy'),
    
    path('progress/', views.list_objective_progress, name='list_objective_progress'),
    path('progress/add/', views.add_objective_progress, name='add_objective_progress'),
    path('progress/<int:id>/', views.edit_objective_progress, name='edit_objective_progress'),
    path('progress/delete/<int:id>/', views.delete_objective_progress, name='delete_objective_progress'),
    

    #Inherent Risk 
    path('inherent_risks/', views.list_inherent_risks, name='list_inherent_risks'),
    path('inherent_risks/add/', views.add_inherent_risk, name='add_inherent_risk'),
    path('inherent_risks/<int:id>/edit/', views.edit_inherent_risk, name='edit_inherent_risk'),
    path('inherent_risks/<int:id>/delete/', views.delete_inherent_risk, name='delete_inherent_risk'),
    
    path('risk_assessments/', views.list_risk_assessments, name='list_risk_assessments'),
    path('risk_assessments/add/', views.add_risk_assessment, name='add_risk_assessment'),
    path('risk_assessments/<int:assessment_id>/edit/', views.edit_risk_assessment, name='edit_risk_assessment'),
    path('risk_assessments/<int:assessment_id>/delete/', views.delete_risk_assessment, name='delete_risk_assessment'),

    #kris
    path('key_risk_indicators/', views.list_key_risk_indicators, name='list_key_risk_indicators'),
    path('key_risk_indicators/add/', views.add_key_risk_indicator, name='add_key_risk_indicator'),
    path('key_risk_indicators/<int:kri_id>/edit/', views.edit_key_risk_indicator, name='edit_key_risk_indicator'),
    path('key_risk_indicators/<int:kri_id>/delete/', views.delete_key_risk_indicator, name='delete_key_risk_indicator'),
    
    path('key_metrics/', views.list_key_metrics, name='list_key_metrics'),
    path('key_metrics/add/', views.add_key_metric, name='add_key_metric'),
    path('key_metrics/<int:metric_id>/edit/', views.edit_key_metric, name='edit_key_metric'),
    path('key_metrics/<int:metric_id>/delete/', views.delete_key_metric, name='delete_key_metric'),

    #Risk Appetite Console
    path('risk_appetites/', views.list_risk_appetites, name='list_risk_appetites'),
    path('risk_appetites/add/', views.add_risk_appetite, name='add_risk_appetite'),
    path('risk_appetites/<int:appetite_id>/edit/', views.edit_risk_appetite, name='edit_risk_appetite'),
    path('risk_appetites/<int:appetite_id>/delete/', views.delete_risk_appetite, name='delete_risk_appetite'),
    
    path('risk_tolerances/', views.list_risk_tolerances, name='list_risk_tolerances'),
    path('risk_tolerances/add/', views.add_risk_tolerance, name='add_risk_tolerance'),
    path('risk_tolerances/<int:tolerance_id>/edit/', views.edit_risk_tolerance, name='edit_risk_tolerance'),
    path('risk_tolerances/<int:tolerance_id>/delete/', views.delete_risk_tolerance, name='delete_risk_tolerance'),

    # Controls Effectiveness
    path('controls_effectiveness/', views.list_controls, name='list_controls'),
    path('controls_effectiveness/add/', views.add_control, name='add_control'),
    path('controls_effectiveness/<int:control_id>/edit/', views.edit_control, name='edit_control'),
    path('controls_effectiveness/<int:control_id>/delete/', views.delete_control, name='delete_control'),
    
    path('control_assessments/', views.list_control_assessments, name='list_control_assessments'),
    path('control_assessments/add/', views.add_control_assessment, name='add_control_assessment'),
    path('control_assessments/<int:assessment_id>/edit/', views.edit_control_assessment, name='edit_control_assessment'),
    path('control_assessments/<int:assessment_id>/delete/', views.delete_control_assessment, name='delete_control_assessment'),
    
    path('control_logs/', views.list_control_logs, name='list_control_logs'),
    path('control_logs/add/', views.add_control_log, name='add_control_log'),
    path('control_logs/<int:log_id>/edit/', views.edit_control_log, name='edit_control_log'),
    path('control_logs/<int:log_id>/delete/', views.delete_control_log, name='delete_control_log'),

    #Residual Risk Zone
    path('residual_risk_zone/', views.list_residual_risks, name='list_residual_risks'),
    path('residual_risk_zone/add/', views.add_residual_risk, name='add_residual_risk'),
    path('residual_risk_zone/<int:residual_risk_id>/edit/', views.edit_residual_risk, name='edit_residual_risk'),
    path('residual_risk_zone/<int:residual_risk_id>/delete/', views.delete_residual_risk, name='delete_residual_risk'),
    
    path('residual_assessment/', views.list_residual_risk_assessments, name='list_residual_risk_assessments'),
    path('residual_assessment/add/', views.add_residual_risk_assessment, name='add_residual_risk_assessment'),
    path('residual_assessment/<int:assessment_id>/edit/', views.edit_residual_risk_assessment, name='edit_residual_risk_assessment'),
    path('residual_assessment/<int:assessment_id>/delete/', views.delete_residual_risk_assessment, name='delete_residual_risk_assessment'),

    #Remediation Actions
    path('remediation_actions/', views.list_remediation_actions, name='list_remediation_actions'),
    path('remediation_actions/add/', views.add_remediation_action, name='add_remediation_action'),
    path('remediation_actions/<int:action_id>/edit/', views.edit_remediation_action, name='edit_remediation_action'),
    path('remediation_actions/<int:action_id>/delete/', views.delete_remediation_action, name='delete_remediation_action'),

    #Risk Radar
    path('risk_radar/', views.list_risk_radar, name='list_risk_radar'),
    path('risk_radar/add/', views.add_risk_radar, name='add_risk_radar'),
    path('risk_radar/<int:radar_id>/edit/', views.edit_risk_radar, name='edit_risk_radar'),
    path('risk_radar/<int:radar_id>/delete/', views.delete_risk_radar, name='delete_risk_radar'),

"""