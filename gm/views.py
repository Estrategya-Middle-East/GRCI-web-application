from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import namedtuple
from .forms import *
from .models import *
from django.db.models import F,Q
from main_app.models import *
import pandas as pd
from django.http import HttpResponse,JsonResponse
from django.apps import apps
from datetime import datetime
from django.views.generic import TemplateView

# Create your views here.
# GM Dashboard View
def dashboard(request):
    components = [
        {"name": "Governance Framework", "icon": "fas fa-cogs", "link": "governance_structures"},  # Cogs for framework and structure
        {"name": "Leadership and Accountability", "icon": "fas fa-users-cog", "link": "leadership_accountabilitys"},  # Users cog for leadership and accountability
        {"name": "Organizational Purpose", "icon": "fas fa-bullseye", "link": "purpose_and_valuess"},  # Bullseye for purpose
        {"name": "Strategy and Direction", "icon": "fas fa-route", "link": "strategic_directions"},  # Route for strategy and direction
        {"name": "Stewardship and Resources", "icon": "fas fa-hand-holding-usd", "link": "resource_managements"},  # Hand holding resources
        {"name": "Risk and Compliance Management", "icon": "fas fa-shield-alt", "link": "risk_and_compliances"},  # Shield for risk and compliance
        {"name": "Performance and Reporting", "icon": "fas fa-chart-line", "link": "performance_reportings"},  # Chart line for performance
        {"name": "Stakeholder Engagement", "icon": "fas fa-users", "link": "stakeholder_engagements"},  # Users for engagement
        {"name": "Ethical Oversight", "icon": "fas fa-balance-scale", "link": "ethical_governances"},  # Balance scale for ethics
        {"name": "Continuous Improvement", "icon": "fas fa-arrow-circle-up", "link": "governance_improvements"},  # Arrow for continuous improvement
        #{"name": "Documentation Management", "icon": "fas fa-folder-open", "link": "#"},  # Folder open for document management
    ]
    context = {
        'page_title': "GM Dashboard",
        'components': components,
    }
    return render(request, 'gm/dashboard.html', context)


#######
def list_governance_structure(request):
    # Get all records by default
    governance_structures = GovernanceStructure.objects.all()
    form = GovernanceStructureForm()

    
    # Default sorting by structure_id
    sort_by = request.GET.get('sort_by', 'structure_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        governance_structures = governance_structures.order_by(sort_by)
    else:
        governance_structures = governance_structures.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(governance_structures, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_governance_structures = paginator.page(page)
    except PageNotAnInteger:
        paginated_governance_structures = paginator.page(1)
    except EmptyPage:
        paginated_governance_structures = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Governance Structure",
        'governance_structures':governance_structures, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_governance_structures': paginated_governance_structures,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': GovernanceStructure._meta.get_field('approval_status').choices,
        'review_frequency_choices': GovernanceStructure._meta.get_field('review_frequency').choices,
        'approver_id_choices': Staff.objects.all(),
        'stewardship_owner_choices': Staff.objects.all(),
    }
    return render(request, 'gm/governance_structure.html', context)


# Add Oversigh 

def add_governance_structure(request):
    form = GovernanceStructureForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Structure added successfully!")
            return redirect('list_governance_structure')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Structure. Please correct the errors.")
    return redirect('list_governance_structure')

# GovernanceStructure Dashboard
def edit_governance_structure(request, structure_id):
    governance_structure = get_object_or_404(GovernanceStructure, structure_id=structure_id)
    if request.method == 'POST':
        form = GovernanceStructureForm(request.POST, instance=governance_structure)
        if form.is_valid():
            form.save()
            messages.success(request, "Structure updated successfully!")
            return redirect('list_governance_structure')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Structure. Please correct the errors.")
    else:
        form = GovernanceStructureForm(instance=governance_structure)
    return render(request, 'gm/governance_structure.html', {'form': form})



# Delete governance_structure
def delete_governance_structure(request, structure_id):
    governance_structure = get_object_or_404(GovernanceStructure, structure_id=structure_id) 
    governance_structure.delete()
    messages.success(request, "Structure deleted successfully!")
    return redirect('list_governance_structure')

def list_leadership_accountability(request):
    # Get all records by default
    leadership_accountabilitys = LeadershipAccountability.objects.all()
    form = LeadershipAccountabilityForm()

    
    # Default sorting by leadership_id
    sort_by = request.GET.get('sort_by', 'leadership_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        leadership_accountabilitys = leadership_accountabilitys.order_by(sort_by)
    else:
        leadership_accountabilitys = leadership_accountabilitys.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(leadership_accountabilitys, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_leadership_accountabilitys = paginator.page(page)
    except PageNotAnInteger:
        paginated_leadership_accountabilitys = paginator.page(1)
    except EmptyPage:
        paginated_leadership_accountabilitys = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Leadership Accountability",
        'leadership_accountabilitys':leadership_accountabilitys, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_leadership_accountabilitys': paginated_leadership_accountabilitys,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': LeadershipAccountability._meta.get_field('approval_status').choices,
        'accountable_to_choices': Staff.objects.all(),
        'role_owner_choices': Staff.objects.all(),
    }
    return render(request, 'gm/leadership_accountability.html', context)


# Add Oversigh 

def add_leadership_accountability(request):
    form = LeadershipAccountabilityForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Accountability added successfully!")
            return redirect('list_leadership_accountability')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Accountability. Please correct the errors.")
    return redirect('list_leadership_accountability')

# LeadershipAccountability Dashboard
def edit_leadership_accountability(request, leadership_id):
    leadership_accountability = get_object_or_404(LeadershipAccountability, leadership_id=leadership_id)
    if request.method == 'POST':
        form = LeadershipAccountabilityForm(request.POST, instance=leadership_accountability)
        if form.is_valid():
            form.save()
            messages.success(request, "Accountability updated successfully!")
            return redirect('list_leadership_accountability')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Accountability. Please correct the errors.")
    else:
        form = LeadershipAccountabilityForm(instance=leadership_accountability)
    return render(request, 'gm/leadership_accountability.html', {'form': form})



# Delete leadership_accountability
def delete_leadership_accountability(request, leadership_id):
    leadership_accountability = get_object_or_404(LeadershipAccountability, leadership_id=leadership_id) 
    leadership_accountability.delete()
    messages.success(request, "Accountability deleted successfully!")
    return redirect('list_leadership_accountability')

########
def list_purpose_and_values(request):
    # Get all records by default
    purpose_and_valuess = PurposeAndValues.objects.all()
    form = PurposeAndValuesForm()

    
    # Default sorting by purpose_id
    sort_by = request.GET.get('sort_by', 'purpose_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        purpose_and_valuess = purpose_and_valuess.order_by(sort_by)
    else:
        purpose_and_valuess = purpose_and_valuess.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(purpose_and_valuess, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_purpose_and_valuess = paginator.page(page)
    except PageNotAnInteger:
        paginated_purpose_and_valuess = paginator.page(1)
    except EmptyPage:
        paginated_purpose_and_valuess = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Purpose And Values",
        'purpose_and_valuess':purpose_and_valuess, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_purpose_and_valuess': paginated_purpose_and_valuess,
        'rows_per_page': rows_per_page,
        'form': form,
        'review_frequency_choices': PurposeAndValues._meta.get_field('review_frequency').choices,
        'stewardship_owner_choices': Staff.objects.all(),
        'approved_by_choices': Staff.objects.all(),
    }
    return render(request, 'gm/purpose_and_values.html', context)


# Add Oversigh 

def add_purpose_and_values(request):
    form = PurposeAndValuesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Purpose added successfully!")
            return redirect('list_purpose_and_values')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Purpose. Please correct the errors.")
    return redirect('list_purpose_and_values')

# PurposeAndValues Dashboard
def edit_purpose_and_values(request, purpose_id):
    purpose_and_values = get_object_or_404(PurposeAndValues, purpose_id=purpose_id)
    if request.method == 'POST':
        form = PurposeAndValuesForm(request.POST, instance=purpose_and_values)
        if form.is_valid():
            form.save()
            messages.success(request, "Purpose updated successfully!")
            return redirect('list_purpose_and_values')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Purpose. Please correct the errors.")
    else:
        form = PurposeAndValuesForm(instance=purpose_and_values)
    return render(request, 'gm/purpose_and_values.html', {'form': form})



# Delete purpose_and_values
def delete_purpose_and_values(request, purpose_id):
    purpose_and_values = get_object_or_404(PurposeAndValues, purpose_id=purpose_id) 
    purpose_and_values.delete()
    messages.success(request, "Purpose deleted successfully!")
    return redirect('list_purpose_and_values')


######
def list_strategic_direction(request):
    # Get all records by default
    strategic_directions = StrategicDirection.objects.all()
    form = StrategicDirectionForm()

    
    # Default sorting by strategy_id
    sort_by = request.GET.get('sort_by', 'strategy_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        strategic_directions = strategic_directions.order_by(sort_by)
    else:
        strategic_directions = strategic_directions.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(strategic_directions, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_strategic_directions = paginator.page(page)
    except PageNotAnInteger:
        paginated_strategic_directions = paginator.page(1)
    except EmptyPage:
        paginated_strategic_directions = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Strategic Direction",
        'strategic_directions':strategic_directions, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_strategic_directions': paginated_strategic_directions,
        'rows_per_page': rows_per_page,
        'form': form,
        'review_frequency_choices': StrategicDirection._meta.get_field('review_frequency').choices,
        'approval_status_choices': StrategicDirection._meta.get_field('approval_status').choices,
        'owner_choices': Staff.objects.all(),
    }
    return render(request, 'gm/strategic_direction.html', context)


# Add Oversigh 

def add_strategic_direction(request):
    form = StrategicDirectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Direction added successfully!")
            return redirect('list_strategic_direction')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Direction. Please correct the errors.")
    return redirect('list_strategic_direction')

# StrategicDirection Dashboard
def edit_strategic_direction(request, strategy_id):
    strategic_direction = get_object_or_404(StrategicDirection, strategy_id=strategy_id)
    if request.method == 'POST':
        form = StrategicDirectionForm(request.POST, instance=strategic_direction)
        if form.is_valid():
            form.save()
            messages.success(request, "Direction updated successfully!")
            return redirect('list_strategic_direction')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Direction. Please correct the errors.")
    else:
        form = StrategicDirectionForm(instance=strategic_direction)
    return render(request, 'gm/strategic_direction.html', {'form': form})



# Delete strategic_direction
def delete_strategic_direction(request, strategy_id):
    strategic_direction = get_object_or_404(StrategicDirection, strategy_id=strategy_id) 
    strategic_direction.delete()
    messages.success(request, "Direction deleted successfully!")
    return redirect('list_strategic_direction')


######
def list_resource_management(request):
    # Get all records by default
    resource_managements = ResourceManagement.objects.all()
    form = ResourceManagementForm()

    
    # Default sorting by resource_id
    sort_by = request.GET.get('sort_by', 'resource_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        resource_managements = resource_managements.order_by(sort_by)
    else:
        resource_managements = resource_managements.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(resource_managements, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_resource_managements = paginator.page(page)
    except PageNotAnInteger:
        paginated_resource_managements = paginator.page(1)
    except EmptyPage:
        paginated_resource_managements = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Resource Management",
        'resource_managements':resource_managements, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_resource_managements': paginated_resource_managements,
        'rows_per_page': rows_per_page,
        'form': form,
        'compliance_status_choices': ResourceManagement._meta.get_field('compliance_status').choices,
        'owner_choices': Staff.objects.all(),
        'allocated_to_choices': Staff.objects.all(),
    }
    return render(request, 'gm/resource_management.html', context)


# Add Oversigh 

def add_resource_management(request):
    form = ResourceManagementForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Resource added successfully!")
            return redirect('list_resource_management')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Resource. Please correct the errors.")
    return redirect('list_resource_management')

# ResourceManagement Dashboard
def edit_resource_management(request, resource_id):
    resource_management = get_object_or_404(ResourceManagement, resource_id=resource_id)
    if request.method == 'POST':
        form = ResourceManagementForm(request.POST, instance=resource_management)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully!")
            return redirect('list_resource_management')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Resource. Please correct the errors.")
    else:
        form = ResourceManagementForm(instance=resource_management)
    return render(request, 'gm/resource_management.html', {'form': form})



# Delete resource_management
def delete_resource_management(request, resource_id):
    resource_management = get_object_or_404(ResourceManagement, resource_id=resource_id) 
    resource_management.delete()
    messages.success(request, "Resource deleted successfully!")
    return redirect('list_resource_management')


#########
def list_risk_and_compliance(request):
    # Get all records by default
    risk_and_compliances = RiskAndCompliance.objects.all()
    form = RiskAndComplianceForm()

    
    # Default sorting by risk_compliance_id
    sort_by = request.GET.get('sort_by', 'risk_compliance_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        risk_and_compliances = risk_and_compliances.order_by(sort_by)
    else:
        risk_and_compliances = risk_and_compliances.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(risk_and_compliances, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_risk_and_compliances = paginator.page(page)
    except PageNotAnInteger:
        paginated_risk_and_compliances = paginator.page(1)
    except EmptyPage:
        paginated_risk_and_compliances = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Risk And Compliance",
        'risk_and_compliances':risk_and_compliances, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_risk_and_compliances': paginated_risk_and_compliances,
        'rows_per_page': rows_per_page,
        'form': form,
        'risk_severity_choices': RiskAndCompliance._meta.get_field('risk_severity').choices,
        'compliance_status_choices': RiskAndCompliance._meta.get_field('compliance_status').choices,
        'review_frequency_choices': RiskAndCompliance._meta.get_field('review_frequency').choices,
        'owner_choices': Staff.objects.all(),
    }
    return render(request, 'gm/risk_and_compliance.html', context)


# Add Oversigh 

def add_risk_and_compliance(request):
    form = RiskAndComplianceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Compliance added successfully!")
            return redirect('list_risk_and_compliance')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Risk Compliance. Please correct the errors.")
    return redirect('list_risk_and_compliance')

# RiskAndCompliance Dashboard
def edit_risk_and_compliance(request, risk_compliance_id):
    risk_and_compliance = get_object_or_404(RiskAndCompliance, risk_compliance_id=risk_compliance_id)
    if request.method == 'POST':
        form = RiskAndComplianceForm(request.POST, instance=risk_and_compliance)
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Compliance updated successfully!")
            return redirect('list_risk_and_compliance')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Risk Compliance. Please correct the errors.")
    else:
        form = RiskAndComplianceForm(instance=risk_and_compliance)
    return render(request, 'gm/risk_and_compliance.html', {'form': form})



# Delete risk_and_compliance
def delete_risk_and_compliance(request, risk_compliance_id):
    risk_and_compliance = get_object_or_404(RiskAndCompliance, risk_compliance_id=risk_compliance_id) 
    risk_and_compliance.delete()
    messages.success(request, "Risk Compliance deleted successfully!")
    return redirect('list_risk_and_compliance')


########
def list_performance_reporting(request):
    # Get all records by default
    performance_reportings = PerformanceReporting.objects.all()
    form = PerformanceReportingForm()

    
    # Default sorting by report_id
    sort_by = request.GET.get('sort_by', 'report_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        performance_reportings = performance_reportings.order_by(sort_by)
    else:
        performance_reportings = performance_reportings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(performance_reportings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_performance_reportings = paginator.page(page)
    except PageNotAnInteger:
        paginated_performance_reportings = paginator.page(1)
    except EmptyPage:
        paginated_performance_reportings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Performance and Reporting",
        'performance_reportings':performance_reportings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_performance_reportings': paginated_performance_reportings,
        'rows_per_page': rows_per_page,
        'form': form,
        'review_frequency_choices': PerformanceReporting._meta.get_field('review_frequency').choices,
        'approved_by_choices': Staff.objects.all(),
        'prepared_by_choices': Staff.objects.all(),
    }
    return render(request, 'gm/performance_reporting.html', context)


# Add Oversigh 

def add_performance_reporting(request):
    form = PerformanceReportingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Performance Report added successfully!")
            return redirect('list_performance_reporting')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Performance Report. Please correct the errors.")
    return redirect('list_performance_reporting')

# PerformanceReporting Dashboard
def edit_performance_reporting(request, report_id):
    performance_reporting = get_object_or_404(PerformanceReporting, report_id=report_id)
    if request.method == 'POST':
        form = PerformanceReportingForm(request.POST, instance=performance_reporting)
        if form.is_valid():
            form.save()
            messages.success(request, "Performance Report updated successfully!")
            return redirect('list_performance_reporting')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Performance Report. Please correct the errors.")
    else:
        form = PerformanceReportingForm(instance=performance_reporting)
    return render(request, 'gm/performance_reporting.html', {'form': form})



# Delete performance_reporting
def delete_performance_reporting(request, report_id):
    performance_reporting = get_object_or_404(PerformanceReporting, report_id=report_id) 
    performance_reporting.delete()
    messages.success(request, "Performance Report deleted successfully!")
    return redirect('list_performance_reporting')


##########
def list_stakeholder_engagement(request):
    # Get all records by default
    stakeholder_engagements = StakeholderEngagement.objects.all()
    form = StakeholderEngagementForm()

    
    # Default sorting by stakeholder_id
    sort_by = request.GET.get('sort_by', 'stakeholder_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        stakeholder_engagements = stakeholder_engagements.order_by(sort_by)
    else:
        stakeholder_engagements = stakeholder_engagements.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(stakeholder_engagements, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_stakeholder_engagements = paginator.page(page)
    except PageNotAnInteger:
        paginated_stakeholder_engagements = paginator.page(1)
    except EmptyPage:
        paginated_stakeholder_engagements = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Stakeholder Engagement",
        'stakeholder_engagements':stakeholder_engagements, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_stakeholder_engagements': paginated_stakeholder_engagements,
        'rows_per_page': rows_per_page,
        'form': form,
        'resolution_status_choices': StakeholderEngagement._meta.get_field('resolution_status').choices,
        'owner_choices': Staff.objects.all(),
    }
    return render(request, 'gm/stakeholder_engagement.html', context)


# Add Oversigh 

def add_stakeholder_engagement(request):
    form = StakeholderEngagementForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Engagement added successfully!")
            return redirect('list_stakeholder_engagement')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Engagement. Please correct the errors.")
    return redirect('list_stakeholder_engagement')

# StakeholderEngagement Dashboard
def edit_stakeholder_engagement(request, stakeholder_id):
    stakeholder_engagement = get_object_or_404(StakeholderEngagement, stakeholder_id=stakeholder_id)
    if request.method == 'POST':
        form = StakeholderEngagementForm(request.POST, instance=stakeholder_engagement)
        if form.is_valid():
            form.save()
            messages.success(request, "Engagement updated successfully!")
            return redirect('list_stakeholder_engagement')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Engagement. Please correct the errors.")
    else:
        form = StakeholderEngagementForm(instance=stakeholder_engagement)
    return render(request, 'gm/stakeholder_engagement.html', {'form': form})



# Delete stakeholder_engagement
def delete_stakeholder_engagement(request, stakeholder_id):
    stakeholder_engagement = get_object_or_404(StakeholderEngagement, stakeholder_id=stakeholder_id) 
    stakeholder_engagement.delete()
    messages.success(request, "Engagement deleted successfully!")
    return redirect('list_stakeholder_engagement')

######
def list_ethical_governance(request):
    # Get all records by default
    ethical_governances = EthicalGovernance.objects.all()
    form = EthicalGovernanceForm()

    
    # Default sorting by ethics_id
    sort_by = request.GET.get('sort_by', 'ethics_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        ethical_governances = ethical_governances.order_by(sort_by)
    else:
        ethical_governances = ethical_governances.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(ethical_governances, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_ethical_governances = paginator.page(page)
    except PageNotAnInteger:
        paginated_ethical_governances = paginator.page(1)
    except EmptyPage:
        paginated_ethical_governances = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Ethical Governance",
        'ethical_governances':ethical_governances, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_ethical_governances': paginated_ethical_governances,
        'rows_per_page': rows_per_page,
        'form': form,
        'resolution_status_choices': EthicalGovernance._meta.get_field('resolution_status').choices,
        'responsible_owner_choices': Staff.objects.all(),
        'incident_reported_by_choices': Staff.objects.all(),
    }
    return render(request, 'gm/ethical_governance.html', context)


# Add Oversigh 

def add_ethical_governance(request):
    form = EthicalGovernanceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Ethical Governance added successfully!")
            return redirect('list_ethical_governance')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Ethical Governance. Please correct the errors.")
    return redirect('list_ethical_governance')

# EthicalGovernance Dashboard
def edit_ethical_governance(request, ethics_id):
    ethical_governance = get_object_or_404(EthicalGovernance, ethics_id=ethics_id)
    if request.method == 'POST':
        form = EthicalGovernanceForm(request.POST, instance=ethical_governance)
        if form.is_valid():
            form.save()
            messages.success(request, "Ethical Governance updated successfully!")
            return redirect('list_ethical_governance')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Ethical Governance. Please correct the errors.")
    else:
        form = EthicalGovernanceForm(instance=ethical_governance)
    return render(request, 'gm/ethical_governance.html', {'form': form})



# Delete ethical_governance
def delete_ethical_governance(request, ethics_id):
    ethical_governance = get_object_or_404(EthicalGovernance, ethics_id=ethics_id) 
    ethical_governance.delete()
    messages.success(request, "Ethical Governance deleted successfully!")
    return redirect('list_ethical_governance')

########
def list_governance_improvement(request):
    # Get all records by default
    governance_improvements = GovernanceImprovement.objects.all()
    form = GovernanceImprovementForm()

    
    # Default sorting by improvement_id
    sort_by = request.GET.get('sort_by', 'improvement_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        governance_improvements = governance_improvements.order_by(sort_by)
    else:
        governance_improvements = governance_improvements.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(governance_improvements, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_governance_improvements = paginator.page(page)
    except PageNotAnInteger:
        paginated_governance_improvements = paginator.page(1)
    except EmptyPage:
        paginated_governance_improvements = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Governance Improvement",
        'governance_improvements':governance_improvements, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_governance_improvements': paginated_governance_improvements,
        'rows_per_page': rows_per_page,
        'form': form,
        'progress_status_choices': GovernanceImprovement._meta.get_field('progress_status').choices,
        'owner_choices': Staff.objects.all(),
    }
    return render(request, 'gm/governance_improvement.html', context)


# Add Oversigh 

def add_governance_improvement(request):
    form = GovernanceImprovementForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Governance Improvement added successfully!")
            return redirect('list_governance_improvement')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Governance Improvement. Please correct the errors.")
    return redirect('list_governance_improvement')

# GovernanceImprovement Dashboard
def edit_governance_improvement(request, improvement_id):
    governance_improvement = get_object_or_404(GovernanceImprovement, improvement_id=improvement_id)
    if request.method == 'POST':
        form = GovernanceImprovementForm(request.POST, instance=governance_improvement)
        if form.is_valid():
            form.save()
            messages.success(request, "Governance Improvement updated successfully!")
            return redirect('list_governance_improvement')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Governance Improvement. Please correct the errors.")
    else:
        form = GovernanceImprovementForm(instance=governance_improvement)
    return render(request, 'gm/governance_improvement.html', {'form': form})



# Delete governance_improvement
def delete_governance_improvement(request, improvement_id):
    governance_improvement = get_object_or_404(GovernanceImprovement, improvement_id=improvement_id) 
    governance_improvement.delete()
    messages.success(request, "Governance Improvement deleted successfully!")
    return redirect('list_governance_improvement')
