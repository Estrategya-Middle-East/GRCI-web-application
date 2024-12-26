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
    path("", views.dashboard, name="gm_dashboard"),  # Default dashboard for GM

    # Governance Framework
    path('governance_structures/', views.list_governance_structure, name='list_governance_structure'),
    path('governance_structures/add/', views.add_governance_structure, name='add_governance_structure'),
    path('governance_structures/<int:structure_id>/edit/', views.edit_governance_structure, name='edit_governance_structure'),
    path('governance_structures/<int:structure_id>/delete/', views.delete_governance_structure, name='delete_governance_structure'),

    # Leadership Accountability
    path('leadership_accountabilitys/', views.list_leadership_accountability, name='list_leadership_accountability'),
    path('leadership_accountabilitys/add/', views.add_leadership_accountability, name='add_leadership_accountability'),
    path('leadership_accountabilitys/<int:leadership_id>/edit/', views.edit_leadership_accountability, name='edit_leadership_accountability'),
    path('leadership_accountabilitys/<int:leadership_id>/delete/', views.delete_leadership_accountability, name='delete_leadership_accountability'),

    # purpose and values
    path('purpose_and_valuess/', views.list_purpose_and_values, name='list_purpose_and_values'),
    path('purpose_and_valuess/add/', views.add_purpose_and_values, name='add_purpose_and_values'),
    path('purpose_and_valuess/<int:purpose_id>/edit/', views.edit_purpose_and_values, name='edit_purpose_and_values'),
    path('purpose_and_valuess/<int:purpose_id>/delete/', views.delete_purpose_and_values, name='delete_purpose_and_values'),

    # Strategic Direction
    path('strategic_directions/', views.list_strategic_direction, name='list_strategic_direction'),
    path('strategic_directions/add/', views.add_strategic_direction, name='add_strategic_direction'),
    path('strategic_directions/<int:strategy_id>/edit/', views.edit_strategic_direction, name='edit_strategic_direction'),
    path('strategic_directions/<int:strategy_id>/delete/', views.delete_strategic_direction, name='delete_strategic_direction'),

    # resource management
    path('resource_managements/', views.list_resource_management, name='list_resource_management'),
    path('resource_managements/add/', views.add_resource_management, name='add_resource_management'),
    path('resource_managements/<int:resource_id>/edit/', views.edit_resource_management, name='edit_resource_management'),
    path('resource_managements/<int:resource_id>/delete/', views.delete_resource_management, name='delete_resource_management'),

    # Risk And Compliance
    path('risk_and_compliances/', views.list_risk_and_compliance, name='list_risk_and_compliance'),
    path('risk_and_compliances/add/', views.add_risk_and_compliance, name='add_risk_and_compliance'),
    path('risk_and_compliances/<int:risk_compliance_id>/edit/', views.edit_risk_and_compliance, name='edit_risk_and_compliance'),
    path('risk_and_compliances/<int:risk_compliance_id>/delete/', views.delete_risk_and_compliance, name='delete_risk_and_compliance'),

    # Performance Reporting
    path('performance_reportings/', views.list_performance_reporting, name='list_performance_reporting'),
    path('performance_reportings/add/', views.add_performance_reporting, name='add_performance_reporting'),
    path('performance_reportings/<int:report_id>/edit/', views.edit_performance_reporting, name='edit_performance_reporting'),
    path('performance_reportings/<int:report_id>/delete/', views.delete_performance_reporting, name='delete_performance_reporting'),

    # Stakeholder Engagement
    path('stakeholder_engagements/', views.list_stakeholder_engagement, name='list_stakeholder_engagement'),
    path('stakeholder_engagements/add/', views.add_stakeholder_engagement, name='add_stakeholder_engagement'),
    path('stakeholder_engagements/<int:stakeholder_id>/edit/', views.edit_stakeholder_engagement, name='edit_stakeholder_engagement'),
    path('stakeholder_engagements/<int:stakeholder_id>/delete/', views.delete_stakeholder_engagement, name='delete_stakeholder_engagement'),

    # Ethical Governance
    path('ethical_governances/', views.list_ethical_governance, name='list_ethical_governance'),
    path('ethical_governances/add/', views.add_ethical_governance, name='add_ethical_governance'),
    path('ethical_governances/<int:ethics_id>/edit/', views.edit_ethical_governance, name='edit_ethical_governance'),
    path('ethical_governances/<int:ethics_id>/delete/', views.delete_ethical_governance, name='delete_ethical_governance'),

    # Governance Improvement
    path('governance_improvements/', views.list_governance_improvement, name='list_governance_improvement'),
    path('governance_improvements/add/', views.add_governance_improvement, name='add_governance_improvement'),
    path('governance_improvements/<int:improvement_id>/edit/', views.edit_governance_improvement, name='edit_governance_improvement'),
    path('governance_improvements/<int:improvement_id>/delete/', views.delete_governance_improvement, name='delete_governance_improvement'),

]


