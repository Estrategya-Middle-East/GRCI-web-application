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
    path("", views.dashboard, name="bcm_dashboard"),  # Default dashboard for IAM
    
    # BCM Governance
    path('bcm_governances/', views.list_bcm_governance, name='list_bcm_governance'),
    path('bcm_governances/add/', views.add_bcm_governance, name='add_bcm_governance'),
    path('bcm_governances/<int:governance_id>/edit/', views.edit_bcm_governance, name='edit_bcm_governance'),
    path('bcm_governances/<int:governance_id>/delete/', views.delete_bcm_governance, name='delete_bcm_governance'),

    # Business Impact Analysis
    path('business_impact_analysiss/', views.list_business_impact_analysis, name='list_business_impact_analysis'),
    path('business_impact_analysiss/add/', views.add_business_impact_analysis, name='add_business_impact_analysis'),
    path('business_impact_analysiss/<int:bia_id>/edit/', views.edit_business_impact_analysis, name='edit_business_impact_analysis'),
    path('business_impact_analysiss/<int:bia_id>/delete/', views.delete_business_impact_analysis, name='delete_business_impact_analysis'),

    # Continuity Risk Assessment
    path('continuity_risk_assessments/', views.list_continuity_risk_assessment, name='list_continuity_risk_assessment'),
    path('continuity_risk_assessments/add/', views.add_continuity_risk_assessment, name='add_continuity_risk_assessment'),
    path('continuity_risk_assessments/<int:risk_assessment_id>/edit/', views.edit_continuity_risk_assessment, name='edit_continuity_risk_assessment'),
    path('continuity_risk_assessments/<int:risk_assessment_id>/delete/', views.delete_continuity_risk_assessment, name='delete_continuity_risk_assessment'),

    # Continuity Strategy
    path('continuity_strategys/', views.list_continuity_strategy, name='list_continuity_strategy'),
    path('continuity_strategys/add/', views.add_continuity_strategy, name='add_continuity_strategy'),
    path('continuity_strategys/<int:strategy_id>/edit/', views.edit_continuity_strategy, name='edit_continuity_strategy'),
    path('continuity_strategys/<int:strategy_id>/delete/', views.delete_continuity_strategy, name='delete_continuity_strategy'),

    # Business Continuity Plan
    path('business_continuity_plans/', views.list_business_continuity_plan, name='list_business_continuity_plan'),
    path('business_continuity_plans/add/', views.add_business_continuity_plan, name='add_business_continuity_plan'),
    path('business_continuity_plans/<int:bcp_id>/edit/', views.edit_business_continuity_plan, name='edit_business_continuity_plan'),
    path('business_continuity_plans/<int:bcp_id>/delete/', views.delete_business_continuity_plan, name='delete_business_continuity_plan'),

    # Continuity Testing
    path('continuity_testings/', views.list_continuity_testing, name='list_continuity_testing'),
    path('continuity_testings/add/', views.add_continuity_testing, name='add_continuity_testing'),
    path('continuity_testings/<int:test_id>/edit/', views.edit_continuity_testing, name='edit_continuity_testing'),
    path('continuity_testings/<int:test_id>/delete/', views.delete_continuity_testing, name='delete_continuity_testing'),

    # Incident Activation
    path('incident_activations/', views.list_incident_activation, name='list_incident_activation'),
    path('incident_activations/add/', views.add_incident_activation, name='add_incident_activation'),
    path('incident_activations/<int:incident_id>/edit/', views.edit_incident_activation, name='edit_incident_activation'),
    path('incident_activations/<int:incident_id>/delete/', views.delete_incident_activation, name='delete_incident_activation'),

    # Crisis Communication
    path('crisis_communications/', views.list_crisis_communication, name='list_crisis_communication'),
    path('crisis_communications/add/', views.add_crisis_communication, name='add_crisis_communication'),
    path('crisis_communications/<int:communication_id>/edit/', views.edit_crisis_communication, name='edit_crisis_communication'),
    path('crisis_communications/<int:communication_id>/delete/', views.delete_crisis_communication, name='delete_crisis_communication'),

    # BCM Program Review
    path('bcm_program_reviews/', views.list_bcm_program_review, name='list_bcm_program_review'),
    path('bcm_program_reviews/add/', views.add_bcm_program_review, name='add_bcm_program_review'),
    path('bcm_program_reviews/<int:review_id>/edit/', views.edit_bcm_program_review, name='edit_bcm_program_review'),
    path('bcm_program_reviews/<int:review_id>/delete/', views.delete_bcm_program_review, name='delete_bcm_program_review'),

]


