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
# IAM Dashboard View
def dashboard(request):
    components = [
        {"name": "Audit Governance and Oversight", "icon": "fas fa-gavel", "link": "audit_oversight/audit_plannings/"},
        {"name": "Risk and Process Analysis", "icon": "fas fa-chart-pie", "link": "risk_mappings"},
        {"name": "Audit Engagement Management", "icon": "fas fa-tasks", "link": "audit_engagement/engagement_plannings/"},
        {"name": "Audit Execution", "icon": "fas fa-check-circle", "link": "audit_executions"},
        {"name": "Audit Follow-Up and Monitoring", "icon": "fas fa-sync-alt", "link": "follow_ups"},
        {"name": "Audit Reporting", "icon": "fas fa-file-alt", "link": "audit_reporting/audit_reports/"},
        {"name": "Audit Quality Assurance", "icon": "fas fa-thumbs-up", "link": "quality_assurances"},
        {"name": "Fraud Detection and Investigation", "icon": "fas fa-search-dollar", "link": "fraud_investigations"},
        #{"name": "Document Management", "icon": "fas fa-folder-open", "link": "#"},
        {"name": "Compliance Monitoring", "icon": "fas fa-shield-alt", "link": "compliance_trackers"},
    ]
    context = {
        'page_title': "IAM Dashboard",
        'components': components,
    }
    return render(request, 'iam/dashboard.html', context)

def audit_oversight_dashboard(request):
    components = [
        {"name": "Audit Planning", "icon": "fas fa-calendar-alt", "link": "audit_plannings"},  # Calendar for planning
        {"name": "Audit Universe Register", "icon": "fas fa-database", "link": "audit_registers"},  # Database for register
    ]
    context = {
        'page_title': "Audit Governance and Oversight",
        'components': components,
    }
    return render(request, 'audit_oversight/dashboard.html', context)


def audit_engagement_dashboard(request):
    components = [
        {"name": "Engagement Planning", "icon": "fas fa-tasks", "link": "engagement_plannings"},  # Tasks for planning engagement
        {"name": "Audit Resource Planner", "icon": "fas fa-users-cog", "link": "audit_resources"},  # Users and cog for resource management
    ]
    context = {
        'page_title': "Audit Engagement Management",
        'components': components,
    }
    return render(request, 'audit_engagement/dashboard.html', context)


def audit_reporting_dashboard(request):
    components = [
        {"name": "Audit Report", "icon": "fas fa-file-alt", "link": "audit_reports"},  # File for reporting
        {"name": "Risk Trends Report", "icon": "fas fa-chart-line", "link": "risktrends_reports"},  # Chart line for trends report
    ]
    context = {
        'page_title': "Audit Reporting",
        'components': components,
    }
    return render(request, 'audit_reporting/dashboard.html', context)


####

def list_audit_planning(request):
    # Get all records by default
    audit_plannings = AuditPlanning.objects.all()
    form = AuditPlanningForm()

    
    # Default sorting by plan_id
    sort_by = request.GET.get('sort_by', 'plan_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_plannings = audit_plannings.order_by(sort_by)
    else:
        audit_plannings = audit_plannings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_plannings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_plannings = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_plannings = paginator.page(1)
    except EmptyPage:
        paginated_audit_plannings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Planning",
        'audit_plannings':audit_plannings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_plannings': paginated_audit_plannings,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': AuditPlanning._meta.get_field('approval_status').choices,
        'audit_frequency_choices': AuditPlanning._meta.get_field('audit_frequency').choices,
        'reviewers': Staff.objects.all(),
    }
    return render(request, 'audit_oversight/audit_planning.html', context)


# Add Oversigh 

def add_audit_planning(request):
    form = AuditPlanningForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan  added successfully!")
            return redirect('list_audit_planning')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Plan. Please correct the errors.")
    return redirect('list_audit_planning')

# Audit Planning Dashboard
def edit_audit_planning(request, plan_id):
    audit_planning = get_object_or_404(AuditPlanning, plan_id=plan_id)
    if request.method == 'POST':
        form = AuditPlanningForm(request.POST, instance=audit_planning)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan updated successfully!")
            return redirect('list_audit_planning')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Plan. Please correct the errors.")
    else:
        form = AuditPlanningForm(instance=audit_planning)
    return render(request, 'audit_oversight/audit_planning.html', {'form': form})



# Delete audit_planning
def delete_audit_planning(request, plan_id):
    audit_planning = get_object_or_404(AuditPlanning, plan_id=plan_id) 
    audit_planning.delete()
    messages.success(request, "Audit Plan deleted successfully!")
    return redirect('list_audit_planning')

####

def list_audit_register(request):
    # Get all records by default
    audit_registers = AuditUniverseRegister.objects.all()
    form = AuditUniverseRegisterForm()

    
    # Default sorting by entity_id
    sort_by = request.GET.get('sort_by', 'entity_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_registers = audit_registers.order_by(sort_by)
    else:
        audit_registers = audit_registers.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_registers, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_registers = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_registers = paginator.page(1)
    except EmptyPage:
        paginated_audit_registers = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Universe Register",
        'audit_registers':audit_registers, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_registers': paginated_audit_registers,
        'rows_per_page': rows_per_page,
        'form': form,
        'audit_cycle_status_choices': AuditUniverseRegister._meta.get_field('audit_cycle_status').choices,
        'audit_frequency_choices': AuditUniverseRegister._meta.get_field('audit_frequency').choices,
        'risk_owners': Staff.objects.all(),
    }
    return render(request, 'audit_oversight/audit_register.html', context)


# Add Oversigh 

def add_audit_register(request):
    form = AuditUniverseRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Register  added successfully!")
            return redirect('list_audit_register')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Register. Please correct the errors.")
    return redirect('list_audit_register')

# Audit Planning Dashboard
def edit_audit_register(request, entity_id):
    audit_register = get_object_or_404(AuditUniverseRegister, entity_id=entity_id)
    if request.method == 'POST':
        form = AuditUniverseRegisterForm(request.POST, instance=audit_register)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Register updated successfully!")
            return redirect('list_audit_register')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Register. Please correct the errors.")
    else:
        form = AuditUniverseRegisterForm(instance=audit_register)
    return render(request, 'audit_oversight/audit_register.html', {'form': form})



# Delete audit_register
def delete_audit_register(request, entity_id):
    audit_register = get_object_or_404(AuditUniverseRegister, entity_id=entity_id) 
    audit_register.delete()
    messages.success(request, "Audit Register deleted successfully!")
    return redirect('list_audit_register')

####

def list_risk_mapping(request):
    # Get all records by default
    risk_mappings = RiskMapping.objects.all()
    form = RiskMappingForm()

    
    # Default sorting by process_id
    sort_by = request.GET.get('sort_by', 'process_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        risk_mappings = risk_mappings.order_by(sort_by)
    else:
        risk_mappings = risk_mappings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(risk_mappings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_risk_mappings = paginator.page(page)
    except PageNotAnInteger:
        paginated_risk_mappings = paginator.page(1)
    except EmptyPage:
        paginated_risk_mappings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Risk Mapping",
        'risk_mappings':risk_mappings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_risk_mappings': paginated_risk_mappings,
        'rows_per_page': rows_per_page,
        'form': form,
        'risk_severity_choices': RiskMapping._meta.get_field('risk_severity').choices,
        'update_frequency_choices': RiskMapping._meta.get_field('update_frequency').choices,
        'owners': Staff.objects.all(),
    }
    return render(request, 'iam/risk_mapping.html', context)


# Add Oversigh 

def add_risk_mapping(request):
    form = RiskMappingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Mapping  added successfully!")
            return redirect('list_risk_mapping')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Risk Mapping. Please correct the errors.")
    return redirect('list_risk_mapping')

# Risk Mapping Dashboard
def edit_risk_mapping(request, process_id):
    risk_mapping = get_object_or_404(RiskMapping, process_id=process_id)
    if request.method == 'POST':
        form = RiskMappingForm(request.POST, instance=risk_mapping)
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Mapping updated successfully!")
            return redirect('list_risk_mapping')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Risk Mapping. Please correct the errors.")
    else:
        form = RiskMappingForm(instance=risk_mapping)
    return render(request, 'iam/risk_mapping.html', {'form': form})



# Delete risk_mapping
def delete_risk_mapping(request, process_id):
    risk_mapping = get_object_or_404(RiskMapping, process_id=process_id) 
    risk_mapping.delete()
    messages.success(request, "Risk Mapping deleted successfully!")
    return redirect('list_risk_mapping')


######
######
def list_engagement_planning(request):
    # Get all records by default
    engagement_plannings = EngagementPlanning.objects.all()
    form = EngagementPlanningForm()

    
    # Default sorting by engagement_id
    sort_by = request.GET.get('sort_by', 'engagement_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        engagement_plannings = engagement_plannings.order_by(sort_by)
    else:
        engagement_plannings = engagement_plannings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(engagement_plannings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_engagement_plannings = paginator.page(page)
    except PageNotAnInteger:
        paginated_engagement_plannings = paginator.page(1)
    except EmptyPage:
        paginated_engagement_plannings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Engagement Planning",
        'engagement_plannings':engagement_plannings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_engagement_plannings': paginated_engagement_plannings,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': EngagementPlanning._meta.get_field('approval_status').choices,
        'auditors': Staff.objects.all(),
    }
    return render(request, 'audit_engagement/engagement_planning.html', context)


# Add Oversigh 

def add_engagement_planning(request):
    form = EngagementPlanningForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan  added successfully!")
            return redirect('list_engagement_planning')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Plan. Please correct the errors.")
    return redirect('list_engagement_planning')

# Engagement Planning Dashboard
def edit_engagement_planning(request, engagement_id):
    engagement_planning = get_object_or_404(EngagementPlanning, engagement_id=engagement_id)
    if request.method == 'POST':
        form = EngagementPlanningForm(request.POST, instance=engagement_planning)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan updated successfully!")
            return redirect('list_engagement_planning')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Plan. Please correct the errors.")
    else:
        form = EngagementPlanningForm(instance=engagement_planning)
    return render(request, 'audit_engagement/engagement_planning.html', {'form': form})



# Delete engagement_planning
def delete_engagement_planning(request, engagement_id):
    engagement_planning = get_object_or_404(EngagementPlanning, engagement_id=engagement_id) 
    engagement_planning.delete()
    messages.success(request, "Audit Plan deleted successfully!")
    return redirect('list_engagement_planning')

######
def list_audit_resource(request):
    # Get all records by default
    audit_resources = AuditResourcePlanner.objects.all()
    form = AuditResourcePlannerForm()

    
    # Default sorting by resource_id
    sort_by = request.GET.get('sort_by', 'resource_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_resources = audit_resources.order_by(sort_by)
    else:
        audit_resources = audit_resources.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_resources, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_resources = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_resources = paginator.page(1)
    except EmptyPage:
        paginated_audit_resources = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Resource",
        'audit_resources':audit_resources, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_resources': paginated_audit_resources,
        'rows_per_page': rows_per_page,
        'form': form,
        'availability_status_choices': AuditResourcePlanner._meta.get_field('availability_status').choices,
        'engagements': EngagementPlanning.objects.all(),
    }
    return render(request, 'audit_engagement/audit_resource.html', context)


# Add Oversigh 

def add_audit_resource(request):
    form = AuditResourcePlannerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan  added successfully!")
            return redirect('list_audit_resource')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Plan. Please correct the errors.")
    return redirect('list_audit_resource')

# Audit Resource Dashboard
def edit_audit_resource(request, resource_id):
    audit_resource = get_object_or_404(AuditResourcePlanner, resource_id=resource_id)
    if request.method == 'POST':
        form = AuditResourcePlannerForm(request.POST, instance=audit_resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan updated successfully!")
            return redirect('list_audit_resource')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Plan. Please correct the errors.")
    else:
        form = AuditResourcePlannerForm(instance=audit_resource)
    return render(request, 'audit_engagement/audit_resource.html', {'form': form})



# Delete audit_resource
def delete_audit_resource(request, resource_id):
    audit_resource = get_object_or_404(AuditResourcePlanner, resource_id=resource_id) 
    audit_resource.delete()
    messages.success(request, "Audit Plan deleted successfully!")
    return redirect('list_audit_resource')

######
def list_audit_execution(request):
    # Get all records by default
    audit_executions = ExecutionLog.objects.all()
    form = ExecutionLogForm()

    
    # Default sorting by execution_id
    sort_by = request.GET.get('sort_by', 'execution_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_executions = audit_executions.order_by(sort_by)
    else:
        audit_executions = audit_executions.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_executions, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_executions = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_executions = paginator.page(1)
    except EmptyPage:
        paginated_audit_executions = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Execution",
        'audit_executions':audit_executions, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_executions': paginated_audit_executions,
        'rows_per_page': rows_per_page,
        'form': form,
        'status_choices': ExecutionLog._meta.get_field('status').choices,
        'engagements': EngagementPlanning.objects.all(),
    }
    return render(request, 'iam/audit_execution.html', context)


# Add Oversigh 

def add_audit_execution(request):
    form = ExecutionLogForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Execution added successfully!")
            return redirect('list_audit_execution')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Execution. Please correct the errors.")
    return redirect('list_audit_execution')

# Audit Execution Dashboard
def edit_audit_execution(request, execution_id):
    audit_execution = get_object_or_404(ExecutionLog, execution_id=execution_id)
    if request.method == 'POST':
        form = ExecutionLogForm(request.POST, instance=audit_execution)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Execution updated successfully!")
            return redirect('list_audit_execution')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Execution. Please correct the errors.")
    else:
        form = ExecutionLogForm(instance=audit_execution)
    return render(request, 'iam/audit_execution.html', {'form': form})



# Delete audit_execution
def delete_audit_execution(request, execution_id):
    audit_execution = get_object_or_404(ExecutionLog, execution_id=execution_id) 
    audit_execution.delete()
    messages.success(request, "Audit Execution deleted successfully!")
    return redirect('list_audit_execution')


######
def list_follow_up(request):
    # Get all records by default
    follow_ups = FollowUp.objects.all()
    form = FollowUpForm()

    
    # Default sorting by follow_up_id
    sort_by = request.GET.get('sort_by', 'follow_up_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        follow_ups = follow_ups.order_by(sort_by)
    else:
        follow_ups = follow_ups.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(follow_ups, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_follow_ups = paginator.page(page)
    except PageNotAnInteger:
        paginated_follow_ups = paginator.page(1)
    except EmptyPage:
        paginated_follow_ups = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "FollowUp",
        'follow_ups':follow_ups, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_follow_ups': paginated_follow_ups,
        'rows_per_page': rows_per_page,
        'form': form,
        'completion_status_choices': FollowUp._meta.get_field('completion_status').choices,
        'assigned_to_choices': Staff.objects.all(),
        'audit_choices': AuditUniverseRegister.objects.all(),
    }
    return render(request, 'iam/follow_up.html', context)


# Add Oversigh 

def add_follow_up(request):
    form = FollowUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "FollowUp added successfully!")
            return redirect('list_follow_up')
        else:
            print(form.errors)
            messages.error(request, "Failed to add FollowUp. Please correct the errors.")
    return redirect('list_follow_up')

# FollowUp Dashboard
def edit_follow_up(request, follow_up_id):
    follow_up = get_object_or_404(FollowUp, follow_up_id=follow_up_id)
    if request.method == 'POST':
        form = FollowUpForm(request.POST, instance=follow_up)
        if form.is_valid():
            form.save()
            messages.success(request, "FollowUp updated successfully!")
            return redirect('list_follow_up')
        else:
            print(form.errors)
            messages.error(request, "Failed to update FollowUp. Please correct the errors.")
    else:
        form = FollowUpForm(instance=follow_up)
    return render(request, 'iam/follow_up.html', {'form': form})



# Delete follow_up
def delete_follow_up(request, follow_up_id):
    follow_up = get_object_or_404(FollowUp, follow_up_id=follow_up_id) 
    follow_up.delete()
    messages.success(request, "FollowUp deleted successfully!")
    return redirect('list_follow_up')

######
def list_audit_report(request):
    # Get all records by default
    audit_reports = AuditReport.objects.all()
    form = AuditReportForm()

    
    # Default sorting by report_id
    sort_by = request.GET.get('sort_by', 'report_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_reports = audit_reports.order_by(sort_by)
    else:
        audit_reports = audit_reports.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_reports, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_reports = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_reports = paginator.page(1)
    except EmptyPage:
        paginated_audit_reports = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Report",
        'audit_reports':audit_reports, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_reports': paginated_audit_reports,
        'rows_per_page': rows_per_page,
        'form': form,
        'created_by_choices': Staff.objects.all(),
        'audit_choices': AuditUniverseRegister.objects.all(),
    }
    return render(request, 'audit_reporting/audit_report.html', context)


# Add Oversigh 

def add_audit_report(request):
    form = AuditReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Report added successfully!")
            return redirect('list_audit_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Report. Please correct the errors.")
    return redirect('list_audit_report')

# AuditReport Dashboard
def edit_audit_report(request, report_id):
    audit_report = get_object_or_404(AuditReport, report_id=report_id)
    if request.method == 'POST':
        form = AuditReportForm(request.POST, instance=audit_report)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Report updated successfully!")
            return redirect('list_audit_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Report. Please correct the errors.")
    else:
        form = AuditReportForm(instance=audit_report)
    return render(request, 'audit_reporting/audit_report.html', {'form': form})



# Delete audit_report
def delete_audit_report(request, report_id):
    audit_report = get_object_or_404(AuditReport, report_id=report_id) 
    audit_report.delete()
    messages.success(request, "AuditReport deleted successfully!")
    return redirect('list_audit_report')

######
def list_risktrends_report(request):
    # Get all records by default
    risktrends_reports = RiskTrendsReport.objects.all()
    form = RiskTrendsReportForm()

    
    # Default sorting by trend_id
    sort_by = request.GET.get('sort_by', 'trend_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        risktrends_reports = risktrends_reports.order_by(sort_by)
    else:
        risktrends_reports = risktrends_reports.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(risktrends_reports, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_risktrends_reports = paginator.page(page)
    except PageNotAnInteger:
        paginated_risktrends_reports = paginator.page(1)
    except EmptyPage:
        paginated_risktrends_reports = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Risk Trends Report",
        'risktrends_reports':risktrends_reports, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_risktrends_reports': paginated_risktrends_reports,
        'rows_per_page': rows_per_page,
        'form': form,
        'owners': Staff.objects.all(),
        'impact_level_choices': RiskTrendsReport._meta.get_field('impact_level').choices,
    }
    return render(request, 'audit_reporting/risktrends_report.html', context)


# Add Oversight 

def add_risktrends_report(request):
    form = RiskTrendsReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Trends Report added successfully!")
            return redirect('list_risktrends_report')
        
        else:
            print(form.errors)
            messages.error(request, "Failed to add Risk Trends Report. Please correct the errors.")
    return redirect('list_risktrends_report')

# RiskTrendsReport Dashboard
def edit_risktrends_report(request, trend_id):
    risktrends_report = get_object_or_404(RiskTrendsReport, trend_id=trend_id)
    if request.method == 'POST':
        form = RiskTrendsReportForm(request.POST, instance=risktrends_report)
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Trends Report updated successfully!")
            return redirect('list_risktrends_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Risk Trends Report. Please correct the errors.")
    else:
        form = RiskTrendsReportForm(instance=risktrends_report)
    return render(request, 'audit_reporting/risktrends_report.html', {'form': form})



# Delete risktrends_report
def delete_risktrends_report(request, trend_id):
    risktrends_report = get_object_or_404(RiskTrendsReport, trend_id=trend_id) 
    risktrends_report.delete()
    messages.success(request, "RiskTrendsReport deleted successfully!")
    return redirect('list_risktrends_report')

######
def list_quality_assurance(request):
    # Get all records by default
    quality_assurances = QualityAssurance.objects.all()
    form = QualityAssuranceForm()

    
    # Default sorting by qa_id
    sort_by = request.GET.get('sort_by', 'qa_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        quality_assurances = quality_assurances.order_by(sort_by)
    else:
        quality_assurances = quality_assurances.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(quality_assurances, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_quality_assurances = paginator.page(page)
    except PageNotAnInteger:
        paginated_quality_assurances = paginator.page(1)
    except EmptyPage:
        paginated_quality_assurances = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Quality Assurance",
        'quality_assurances':quality_assurances, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_quality_assurances': paginated_quality_assurances,
        'rows_per_page': rows_per_page,
        'form': form,
        'compliance_status_choices': QualityAssurance._meta.get_field('compliance_status').choices,
        'implementation_status_choices': QualityAssurance._meta.get_field('implementation_status').choices,
        'audit_choices': AuditUniverseRegister.objects.all(),
        'reviewers': Staff.objects.all(),
    }
    return render(request, 'iam/quality_assurance.html', context)


# Add Oversigh 

def add_quality_assurance(request):
    form = QualityAssuranceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Quality Assurance added successfully!")
            return redirect('list_quality_assurance')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Quality Assurance. Please correct the errors.")
    return redirect('list_quality_assurance')

# QualityAssurance Dashboard
def edit_quality_assurance(request, qa_id):
    quality_assurance = get_object_or_404(QualityAssurance, qa_id=qa_id)
    if request.method == 'POST':
        form = QualityAssuranceForm(request.POST, instance=quality_assurance)
        if form.is_valid():
            form.save()
            messages.success(request, "Quality Assurance updated successfully!")
            return redirect('list_quality_assurance')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Quality Assurance. Please correct the errors.")
    else:
        form = QualityAssuranceForm(instance=quality_assurance)
    return render(request, 'iam/quality_assurance.html', {'form': form})



# Delete quality_assurance
def delete_quality_assurance(request, qa_id):
    quality_assurance = get_object_or_404(QualityAssurance, qa_id=qa_id) 
    quality_assurance.delete()
    messages.success(request, "Quality Assurance deleted successfully!")
    return redirect('list_quality_assurance')


######
def list_fraud_investigation(request):
    # Get all records by default
    fraud_investigations = FraudInvestigationLog.objects.all()
    form = FraudInvestigationLogForm()

    
    # Default sorting by investigation_id
    sort_by = request.GET.get('sort_by', 'investigation_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        fraud_investigations = fraud_investigations.order_by(sort_by)
    else:
        fraud_investigations = fraud_investigations.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(fraud_investigations, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_fraud_investigations = paginator.page(page)
    except PageNotAnInteger:
        paginated_fraud_investigations = paginator.page(1)
    except EmptyPage:
        paginated_fraud_investigations = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Fraud Investigation",
        'fraud_investigations':fraud_investigations, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_fraud_investigations': paginated_fraud_investigations,
        'rows_per_page': rows_per_page,
        'form': form,
        'status_choices': FraudInvestigationLog._meta.get_field('status').choices,
        'reported_by_choices': Staff.objects.all(),
    }
    return render(request, 'iam/fraud_investigation.html', context)


# Add Oversigh 

def add_fraud_investigation(request):
    form = FraudInvestigationLogForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Fraud Investigation added successfully!")
            return redirect('list_fraud_investigation')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Fraud Investigation. Please correct the errors.")
    return redirect('list_fraud_investigation')

# FraudInvestigationLog Dashboard
def edit_fraud_investigation(request, investigation_id):
    fraud_investigation = get_object_or_404(FraudInvestigationLog, investigation_id=investigation_id)
    if request.method == 'POST':
        form = FraudInvestigationLogForm(request.POST, instance=fraud_investigation)
        if form.is_valid():
            form.save()
            messages.success(request, "Fraud Investigation updated successfully!")
            return redirect('list_fraud_investigation')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Fraud Investigation. Please correct the errors.")
    else:
        form = FraudInvestigationLogForm(instance=fraud_investigation)
    return render(request, 'iam/fraud_investigation.html', {'form': form})



# Delete fraud_investigation
def delete_fraud_investigation(request, investigation_id):
    fraud_investigation = get_object_or_404(FraudInvestigationLog, investigation_id=investigation_id) 
    fraud_investigation.delete()
    messages.success(request, "Fraud Investigation deleted successfully!")
    return redirect('list_fraud_investigation')

######
def list_compliance_tracker(request):
    # Get all records by default
    compliance_trackers = ComplianceTracker.objects.all()
    form = ComplianceTrackerForm()

    
    # Default sorting by compliance_id
    sort_by = request.GET.get('sort_by', 'compliance_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        compliance_trackers = compliance_trackers.order_by(sort_by)
    else:
        compliance_trackers = compliance_trackers.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(compliance_trackers, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_compliance_trackers = paginator.page(page)
    except PageNotAnInteger:
        paginated_compliance_trackers = paginator.page(1)
    except EmptyPage:
        paginated_compliance_trackers = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Compliance Tracker",
        'compliance_trackers':compliance_trackers, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_compliance_trackers': paginated_compliance_trackers,
        'rows_per_page': rows_per_page,
        'form': form,
        'compliance_rating_choices': ComplianceTracker._meta.get_field('compliance_rating').choices,
        'compliance_status_choices': ComplianceTracker._meta.get_field('compliance_status').choices,
        'review_frequency_choices': ComplianceTracker._meta.get_field('review_frequency').choices,
        'assigned_owner_choices': Staff.objects.all(),
    }
    return render(request, 'iam/compliance_tracker.html', context)


# Add Oversigh 

def add_compliance_tracker(request):
    form = ComplianceTrackerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Compliance Tracker added successfully!")
            return redirect('list_compliance_tracker')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Compliance Tracker. Please correct the errors.")
    return redirect('list_compliance_tracker')

# ComplianceTracker Dashboard
def edit_compliance_tracker(request, compliance_id):
    compliance_tracker = get_object_or_404(ComplianceTracker, compliance_id=compliance_id)
    if request.method == 'POST':
        form = ComplianceTrackerForm(request.POST, instance=compliance_tracker)
        if form.is_valid():
            form.save()
            messages.success(request, "Compliance Tracker updated successfully!")
            return redirect('list_compliance_tracker')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Compliance Tracker. Please correct the errors.")
    else:
        form = ComplianceTrackerForm(instance=compliance_tracker)
    return render(request, 'iam/compliance_tracker.html', {'form': form})



# Delete compliance_tracker
def delete_compliance_tracker(request, compliance_id):
    compliance_tracker = get_object_or_404(ComplianceTracker, compliance_id=compliance_id) 
    compliance_tracker.delete()
    messages.success(request, "Compliance Tracker deleted successfully!")
    return redirect('list_compliance_tracker')
