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
        {"name": "Macro Planning", "icon": "fas fa-gavel", "link": "macro_planning/audit_plans/"},
        {"name": "Micro Planning", "icon": "fas fa-tasks", "link": "micro_planning/audit_assessments/"},
        {"name": "FieldWork", "icon": "fas fa-chart-pie", "link": "fieldwork/working_papers/"},
        {"name": "Reporting", "icon": "fas fa-check-circle", "link": "#"},
        {"name": "Feedback", "icon": "fas fa-sync-alt", "link": "#"},
        {"name": "Audit Follow-Up", "icon": "fas fa-file-alt", "link": "#"},
        
    ]
    context = {
        'page_title': "IAM Dashboard",
        'components': components,
    }
    return render(request, 'iam/dashboard.html', context)

def macro_planning_dashboard(request):
    components = [
        {"name": "Audit Planning", "icon": "fas fa-calendar-alt", "link": "audit_plannings"},  # Calendar for planning
        {"name": "Audit Universe Register", "icon": "fas fa-database", "link": "audit_registers"},  # Database for register
    ]
    context = {
        'page_title': "Audit Governance and Oversight",
        'components': components,
    }
    return render(request, 'macro_planning/dashboard.html', context)


def micro_planning_dashboard(request):
    components = [
        {"name": "Audit Assessment", "icon": "fas fa-tasks", "link": "audit_assessments"},  # Tasks for planning engagement
        {"name": "Audit Notification Planner", "icon": "fas fa-users-cog", "link": "audit_notifications"},  # Users and cog for resource management
    ]
    context = {
        'page_title': "Audit Engagement Management",
        'components': components,
    }
    return render(request, 'micro_planning/dashboard.html', context)


def audit_programing_dashboard(request):
    components = [
        {"name": "Audit Program", "icon": "fas fa-file-alt", "link": "audit_programs"},  # File for reporting
        {"name": "Working Paper", "icon": "fas fa-chart-line", "link": "working_papers"},  # Chart line for trends report
    ]
    context = {
        'page_title': "Audit Programing",
        'components': components,
    }
    return render(request, 'audit_programing/dashboard.html', context)


#### Macro Planning ####

def list_audit_register(request):
    # Get all records by default
    audit_registers = AuditUniverse.objects.all()
    form = AuditUniverseForm()

    
    # Default sorting by audit_id
    sort_by = request.GET.get('sort_by', 'audit_id')
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
        'risk_category_choices': AuditUniverse._meta.get_field('risk_category').choices,
        'priority_level_choices': AuditUniverse._meta.get_field('priority_level').choices,
        'assigned_auditors': Staff.objects.all(),
    }
    return render(request, 'macro_planning/audit_register.html', context)


# Add Oversigh 

def add_audit_register(request):
    form = AuditUniverseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Register  added successfully!")
            return redirect('list_audit_register')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Register. Please correct the errors.")
    return redirect('list_audit_register')

# Audit Planning 
def edit_audit_register(request, audit_id):
    audit_register = get_object_or_404(AuditUniverse, audit_id=audit_id)
    if request.method == 'POST':
        form = AuditUniverseForm(request.POST, instance=audit_register)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Register updated successfully!")
            return redirect('list_audit_register')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Register. Please correct the errors.")
    else:
        form = AuditUniverseForm(instance=audit_register)
    return render(request, 'macro_planning/audit_register.html', {'form': form})



# Delete audit_register
def delete_audit_register(request, audit_id):
    audit_register = get_object_or_404(AuditUniverse, audit_id=audit_id) 
    audit_register.delete()
    messages.success(request, "Audit Register deleted successfully!")
    return redirect('list_audit_register')

####

def list_risk_assessment(request):
    # Get all records by default
    risk_assessments = RiskAssessment.objects.all()
    form = RiskAssessmentForm()

    
    # Default sorting by risk_id
    sort_by = request.GET.get('sort_by', 'risk_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        risk_assessments = risk_assessments.order_by(sort_by)
    else:
        risk_assessments = risk_assessments.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(risk_assessments, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_risk_assessments = paginator.page(page)
    except PageNotAnInteger:
        paginated_risk_assessments = paginator.page(1)
    except EmptyPage:
        paginated_risk_assessments = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Risk Assessment",
        'risk_assessments':risk_assessments, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_risk_assessments': paginated_risk_assessments,
        'rows_per_page': rows_per_page,
        'form': form,
        'risk_severity_choices': RiskAssessment._meta.get_field('risk_severity').choices,
        'risk_type_choices': RiskAssessment._meta.get_field('risk_type').choices,
        'assessed_bys': Staff.objects.all(),
    }
    return render(request, 'macro_planning/risk_assessment.html', context)


# Add Oversigh 

def add_risk_assessment(request):
    form = RiskAssessmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Assessment  added successfully!")
            return redirect('list_risk_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Risk Assessment. Please correct the errors.")
    return redirect('list_risk_assessment')

# Risk Assessment 
def edit_risk_assessment(request, risk_id):
    risk_assessment = get_object_or_404(RiskAssessment, risk_id=risk_id)
    if request.method == 'POST':
        form = RiskAssessmentForm(request.POST, instance=risk_assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Assessment updated successfully!")
            return redirect('list_risk_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Risk Assessment. Please correct the errors.")
    else:
        form = RiskAssessmentForm(instance=risk_assessment)
    return render(request, 'macro_planning/risk_assessment.html', {'form': form})



# Delete risk_assessment
def delete_risk_assessment(request, risk_id):
    risk_assessment = get_object_or_404(RiskAssessment, risk_id=risk_id) 
    risk_assessment.delete()
    messages.success(request, "Risk Assessment deleted successfully!")
    return redirect('list_risk_assessment')

####

def list_audit_plan(request):
    # Get all records by default
    audit_plans = AuditPlan.objects.all()
    form = AuditPlanForm()

    
    # Default sorting by plan_id
    sort_by = request.GET.get('sort_by', 'plan_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_plans = audit_plans.order_by(sort_by)
    else:
        audit_plans = audit_plans.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_plans, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_plans = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_plans = paginator.page(1)
    except EmptyPage:
        paginated_audit_plans = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Plan",
        'audit_plans':audit_plans, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_plans': paginated_audit_plans,
        'rows_per_page': rows_per_page,
        'form': form,
        'priority_level_choices': AuditPlan._meta.get_field('priority_level').choices,
        'audit_frequency_choices': AuditPlan._meta.get_field('audit_frequency').choices,
        'assigned_teams': Staff.objects.all(),
    }
    return render(request, 'macro_planning/audit_plan.html', context)


# Add Oversigh 

def add_audit_plan(request):
    form = AuditPlanForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan  added successfully!")
            return redirect('list_audit_plan')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Plan. Please correct the errors.")
    return redirect('list_audit_plan')

# Audit Plan 
def edit_audit_plan(request, plan_id):
    audit_plan = get_object_or_404(AuditPlan, plan_id=plan_id)
    if request.method == 'POST':
        form = AuditPlanForm(request.POST, instance=audit_plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Plan updated successfully!")
            return redirect('list_audit_plan')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Plan. Please correct the errors.")
    else:
        form = AuditPlanForm(instance=audit_plan)
    return render(request, 'macro_planning/audit_plan.html', {'form': form})



# Delete audit_plan
def delete_audit_plan(request, plan_id):
    audit_plan = get_object_or_404(AuditPlan, plan_id=plan_id) 
    audit_plan.delete()
    messages.success(request, "Audit Plan deleted successfully!")
    return redirect('list_audit_plan')



### Micro Planning ###

######
def list_audit_assessment(request):
    # Get all records by default
    audit_assessments = AuditAssessment.objects.all()
    form = AuditAssessmentForm()

    
    # Default sorting by assessment_id
    sort_by = request.GET.get('sort_by', 'assessment_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_assessments = audit_assessments.order_by(sort_by)
    else:
        audit_assessments = audit_assessments.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_assessments, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_assessments = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_assessments = paginator.page(1)
    except EmptyPage:
        paginated_audit_assessments = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Assessment",
        'audit_assessments':audit_assessments, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_assessments': paginated_audit_assessments,
        'rows_per_page': rows_per_page,
        'form': form,
        'auditors': Staff.objects.all(),
    }
    return render(request, 'micro_planning/audit_assessment.html', context)


# Add Oversigh 

def add_audit_assessment(request):
    form = AuditAssessmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Assessment  added successfully!")
            return redirect('list_audit_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Assessment. Please correct the errors.")
    return redirect('list_audit_assessment')

# Audit Assessment 
def edit_audit_assessment(request, assessment_id):
    audit_assessment = get_object_or_404(AuditAssessment, assessment_id=assessment_id)
    if request.method == 'POST':
        form = AuditAssessmentForm(request.POST, instance=audit_assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Assessment updated successfully!")
            return redirect('list_audit_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Assessment. Please correct the errors.")
    else:
        form = AuditAssessmentForm(instance=audit_assessment)
    return render(request, 'micro_planning/audit_assessment.html', {'form': form})



# Delete audit_assessment
def delete_audit_assessment(request, assessment_id):
    audit_assessment = get_object_or_404(AuditAssessment, assessment_id=assessment_id) 
    audit_assessment.delete()
    messages.success(request, "Audit Assessment deleted successfully!")
    return redirect('list_audit_assessment')

######
def list_audit_notification(request):
    # Get all records by default
    audit_notifications = AuditNotification.objects.all()
    form = AuditNotificationForm()

    
    # Default sorting by notification_id
    sort_by = request.GET.get('sort_by', 'notification_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_notifications = audit_notifications.order_by(sort_by)
    else:
        audit_notifications = audit_notifications.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_notifications, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_notifications = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_notifications = paginator.page(1)
    except EmptyPage:
        paginated_audit_notifications = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Notification",
        'audit_notifications':audit_notifications, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_notifications': paginated_audit_notifications,
        'rows_per_page': rows_per_page,
        'form': form,
        'engagements': Staff.objects.all(),
    }
    return render(request, 'micro_planning/audit_notification.html', context)


# Add Oversigh 

def add_audit_notification(request):
    form = AuditNotificationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Notification  added successfully!")
            return redirect('list_audit_notification')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Notification. Please correct the errors.")
    return redirect('list_audit_notification')

# Audit Notification 
def edit_audit_notification(request, notification_id):
    audit_notification = get_object_or_404(AuditNotification, notification_id=notification_id)
    if request.method == 'POST':
        form = AuditNotificationForm(request.POST, instance=audit_notification)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Notification updated successfully!")
            return redirect('list_audit_notification')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Notification. Please correct the errors.")
    else:
        form = AuditNotificationForm(instance=audit_notification)
    return render(request, 'micro_planning/audit_notification.html', {'form': form})



# Delete audit_notification
def delete_audit_notification(request, notification_id):
    audit_notification = get_object_or_404(AuditNotification, notification_id=notification_id) 
    audit_notification.delete()
    messages.success(request, "Audit Notification deleted successfully!")
    return redirect('list_audit_notification')

######
def list_entrance_meeting(request):
    # Get all records by default
    entrance_meetings = EntranceMeeting.objects.all()
    form = EntranceMeetingForm()

    
    # Default sorting by meeting_id
    sort_by = request.GET.get('sort_by', 'meeting_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        entrance_meetings = entrance_meetings.order_by(sort_by)
    else:
        entrance_meetings = entrance_meetings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(entrance_meetings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_entrance_meetings = paginator.page(page)
    except PageNotAnInteger:
        paginated_entrance_meetings = paginator.page(1)
    except EmptyPage:
        paginated_entrance_meetings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Entrance Meeting",
        'entrance_meetings':entrance_meetings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_entrance_meetings': paginated_entrance_meetings,
        'rows_per_page': rows_per_page,
        'form': form,
        'engagements': Staff.objects.all(),
    }
    return render(request, 'micro_planning/entrance_meeting.html', context)


# Add Oversigh 

def add_entrance_meeting(request):
    form = EntranceMeetingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Entrance Meeting added successfully!")
            return redirect('list_entrance_meeting')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Entrance Meeting. Please correct the errors.")
    return redirect('list_entrance_meeting')

# Entrance Meeting 
def edit_entrance_meeting(request, meeting_id):
    entrance_meeting = get_object_or_404(EntranceMeeting, meeting_id=meeting_id)
    if request.method == 'POST':
        form = EntranceMeetingForm(request.POST, instance=entrance_meeting)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrance Meeting updated successfully!")
            return redirect('list_entrance_meeting')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Entrance Meeting. Please correct the errors.")
    else:
        form = EntranceMeetingForm(instance=entrance_meeting)
    return render(request, 'micro_planning/entrance_meeting.html', {'form': form})



# Delete entrance_meeting
def delete_entrance_meeting(request, meeting_id):
    entrance_meeting = get_object_or_404(EntranceMeeting, meeting_id=meeting_id) 
    entrance_meeting.delete()
    messages.success(request, "Entrance Meeting deleted successfully!")
    return redirect('list_entrance_meeting')


######
def list_sub_risk_assessment(request):
    # Get all records by default
    sub_risk_assessments = SubRiskAssessment.objects.all()
    form = SubRiskAssessmentForm()

    
    # Default sorting by assessment_id
    sort_by = request.GET.get('sort_by', 'assessment_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        sub_risk_assessments = sub_risk_assessments.order_by(sort_by)
    else:
        sub_risk_assessments = sub_risk_assessments.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(sub_risk_assessments, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_sub_risk_assessments = paginator.page(page)
    except PageNotAnInteger:
        paginated_sub_risk_assessments = paginator.page(1)
    except EmptyPage:
        paginated_sub_risk_assessments = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Sub-Process Risk Assessment",
        'sub_risk_assessments':sub_risk_assessments, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_sub_risk_assessments': paginated_sub_risk_assessments,
        'rows_per_page': rows_per_page,
        'form': form,
        'risk_severity_choices': SubRiskAssessment._meta.get_field('risk_severity').choices,
        'risk_category_choices': SubRiskAssessment._meta.get_field('risk_category').choices,
        'assessed_bys': Staff.objects.all(),
    }
    return render(request, 'micro_planning/sub_risk_assessment.html', context)


# Add Oversigh 

def add_sub_risk_assessment(request):
    form = SubRiskAssessmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "SubRisk Assessment added successfully!")
            return redirect('list_sub_risk_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to add SubRiskAssessment. Please correct the errors.")
    return redirect('list_sub_risk_assessment')

# SubRiskAssessment 
def edit_sub_risk_assessment(request, assessment_id):
    sub_risk_assessment = get_object_or_404(SubRiskAssessment, assessment_id=assessment_id)
    if request.method == 'POST':
        form = SubRiskAssessmentForm(request.POST, instance=sub_risk_assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "SubRisk Assessment updated successfully!")
            return redirect('list_sub_risk_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to update SubRisk Assessment. Please correct the errors.")
    else:
        form = SubRiskAssessmentForm(instance=sub_risk_assessment)
    return render(request, 'micro_planning/sub_risk_assessment.html', {'form': form})



# Delete sub_risk_assessment
def delete_sub_risk_assessment(request, assessment_id):
    sub_risk_assessment = get_object_or_404(SubRiskAssessment, assessment_id=assessment_id) 
    sub_risk_assessment.delete()
    messages.success(request, "SubRisk Assessment deleted successfully!")
    return redirect('list_sub_risk_assessment')

######
def list_audit_program(request):
    # Get all records by default
    audit_programs = AuditProgram.objects.all()
    form = AuditProgramForm()

    
    # Default sorting by program_id
    sort_by = request.GET.get('sort_by', 'program_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_programs = audit_programs.order_by(sort_by)
    else:
        audit_programs = audit_programs.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_programs, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_programs = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_programs = paginator.page(1)
    except EmptyPage:
        paginated_audit_programs = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Program",
        'audit_programs':audit_programs, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_programs': paginated_audit_programs,
        'rows_per_page': rows_per_page,
        'form': form,
        'owners': Staff.objects.all(),
        'sub_process_choices': SubRiskAssessment.objects.all(),
    }
    return render(request, 'micro_planning/audit_program.html', context)


# Add Oversigh 

def add_audit_program(request):
    form = AuditProgramForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Program added successfully!")
            return redirect('list_audit_program')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Program. Please correct the errors.")
    return redirect('list_audit_program')

# Audit Program 
def edit_audit_program(request, program_id):
    audit_program = get_object_or_404(AuditProgram, program_id=program_id)
    if request.method == 'POST':
        form = AuditProgramForm(request.POST, instance=audit_program)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Program updated successfully!")
            return redirect('list_audit_program')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Program. Please correct the errors.")
    else:
        form = AuditProgramForm(instance=audit_program)
    return render(request, 'micro_planning/audit_program.html', {'form': form})



# Delete audit_program
def delete_audit_program(request, program_id):
    audit_program = get_object_or_404(AuditProgram, program_id=program_id) 
    audit_program.delete()
    messages.success(request, "Audit Program deleted successfully!")
    return redirect('list_audit_program')

######
def list_working_paper(request):
    # Get all records by default
    working_papers = WorkingPaper.objects.all()
    form = WorkingPaperForm()

    
    # Default sorting by working_paper_id
    sort_by = request.GET.get('sort_by', 'working_paper_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        working_papers = working_papers.order_by(sort_by)
    else:
        working_papers = working_papers.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(working_papers, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_working_papers = paginator.page(page)
    except PageNotAnInteger:
        paginated_working_papers = paginator.page(1)
    except EmptyPage:
        paginated_working_papers = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Working Paper",
        'working_papers':working_papers, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_working_papers': paginated_working_papers,
        'rows_per_page': rows_per_page,
        'form': form,
        'performed_by_choices': Staff.objects.all(),
    }
    return render(request, 'fieldwork/working_paper.html', context)


# Add Oversight 

def add_working_paper(request):
    form = WorkingPaperForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Working Paper added successfully!")
            return redirect('list_working_paper')
        
        else:
            print(form.errors)
            messages.error(request, "Failed to add Working Paper. Please correct the errors.")
    return redirect('list_working_paper')

# WorkingPaper 
def edit_working_paper(request, working_paper_id):
    working_paper = get_object_or_404(WorkingPaper, working_paper_id=working_paper_id)
    if request.method == 'POST':
        form = WorkingPaperForm(request.POST, instance=working_paper)
        if form.is_valid():
            form.save()
            messages.success(request, "Working Paper updated successfully!")
            return redirect('list_working_paper')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Working Paper. Please correct the errors.")
    else:
        form = WorkingPaperForm(instance=working_paper)
    return render(request, 'fieldwork/working_paper.html', {'form': form})



# Delete working_paper
def delete_working_paper(request, working_paper_id):
    working_paper = get_object_or_404(WorkingPaper, working_paper_id=working_paper_id) 
    working_paper.delete()
    messages.success(request, "WorkingPaper deleted successfully!")
    return redirect('list_working_paper')

######
def list_observation_sheet(request):
    # Get all records by default
    observation_sheets = ObservationSheet.objects.all()
    form = ObservationSheetForm()

    
    # Default sorting by observation_id
    sort_by = request.GET.get('sort_by', 'observation_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        observation_sheets = observation_sheets.order_by(sort_by)
    else:
        observation_sheets = observation_sheets.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(observation_sheets, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_observation_sheets = paginator.page(page)
    except PageNotAnInteger:
        paginated_observation_sheets = paginator.page(1)
    except EmptyPage:
        paginated_observation_sheets = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Observation Sheet",
        'observation_sheets':observation_sheets, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_observation_sheets': paginated_observation_sheets,
        'rows_per_page': rows_per_page,
        'form': form,
        'assigned_tos': Staff.objects.all(),
    }
    return render(request, 'fieldwork/observation_sheet.html', context)


# Add Oversigh 

def add_observation_sheet(request):
    form = ObservationSheetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Observation Sheet added successfully!")
            return redirect('list_observation_sheet')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Observation Sheet. Please correct the errors.")
    return redirect('list_observation_sheet')

# ObservationSheet 
def edit_observation_sheet(request, observation_id):
    observation_sheet = get_object_or_404(ObservationSheet, observation_id=observation_id)
    if request.method == 'POST':
        form = ObservationSheetForm(request.POST, instance=observation_sheet)
        if form.is_valid():
            form.save()
            messages.success(request, "Observation Sheet updated successfully!")
            return redirect('list_observation_sheet')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Observation Sheet. Please correct the errors.")
    else:
        form = ObservationSheetForm(instance=observation_sheet)
    return render(request, 'fieldwork/observation_sheet.html', {'form': form})



# Delete observation_sheet
def delete_observation_sheet(request, observation_id):
    observation_sheet = get_object_or_404(ObservationSheet, observation_id=observation_id) 
    observation_sheet.delete()
    messages.success(request, "Observation Sheet deleted successfully!")
    return redirect('list_observation_sheet')


######
def list_other_notes(request):
    # Get all records by default
    other_notess = OtherNotes.objects.all()
    form = OtherNotesForm()

    
    # Default sorting by note_id
    sort_by = request.GET.get('sort_by', 'note_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        other_notess = other_notess.order_by(sort_by)
    else:
        other_notess = other_notess.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(other_notess, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_other_notess = paginator.page(page)
    except PageNotAnInteger:
        paginated_other_notess = paginator.page(1)
    except EmptyPage:
        paginated_other_notess = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Other Notes",
        'other_notess':other_notess, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_other_notess': paginated_other_notess,
        'rows_per_page': rows_per_page,
        'form': form,
        'added_by_choices': Staff.objects.all(),
    }
    return render(request, 'fieldwork/other_notes.html', context)


# Add Oversigh 

def add_other_notes(request):
    form = OtherNotesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Other Notes added successfully!")
            return redirect('list_other_notes')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Other Notes. Please correct the errors.")
    return redirect('list_other_notes')

# OtherNotes 
def edit_other_notes(request, note_id):
    other_notes = get_object_or_404(OtherNotes, note_id=note_id)
    if request.method == 'POST':
        form = OtherNotesForm(request.POST, instance=other_notes)
        if form.is_valid():
            form.save()
            messages.success(request, "Other Notes updated successfully!")
            return redirect('list_other_notes')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Other Notes. Please correct the errors.")
    else:
        form = OtherNotesForm(instance=other_notes)
    return render(request, 'fieldwork/other_notes.html', {'form': form})



# Delete other_notes
def delete_other_notes(request, note_id):
    other_notes = get_object_or_404(OtherNotes, note_id=note_id) 
    other_notes.delete()
    messages.success(request, "Other Notes deleted successfully!")
    return redirect('list_other_notes')

######
def list_exit_meeting(request):
    # Get all records by default
    exit_meetings = ExitMeeting.objects.all()
    form = ExitMeetingForm()

    
    # Default sorting by meeting_id
    sort_by = request.GET.get('sort_by', 'meeting_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        exit_meetings = exit_meetings.order_by(sort_by)
    else:
        exit_meetings = exit_meetings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(exit_meetings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_exit_meetings = paginator.page(page)
    except PageNotAnInteger:
        paginated_exit_meetings = paginator.page(1)
    except EmptyPage:
        paginated_exit_meetings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Exit Meeting",
        'exit_meetings':exit_meetings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_exit_meetings': paginated_exit_meetings,
        'rows_per_page': rows_per_page,
        'form': form,
        'engagements': Staff.objects.all(),
    }
    return render(request, 'audit_reporting/exit_meeting.html', context)


# Add Oversigh 

def add_exit_meeting(request):
    form = ExitMeetingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Exit Meeting added successfully!")
            return redirect('list_exit_meeting')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Exit Meeting. Please correct the errors.")
    return redirect('list_exit_meeting')

# Exit Meeting 
def edit_exit_meeting(request, meeting_id):
    exit_meeting = get_object_or_404(ExitMeeting, meeting_id=meeting_id)
    if request.method == 'POST':
        form = ExitMeetingForm(request.POST, instance=exit_meeting)
        if form.is_valid():
            form.save()
            messages.success(request, "Exit Meeting updated successfully!")
            return redirect('list_exit_meeting')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Exit Meeting. Please correct the errors.")
    else:
        form = ExitMeetingForm(instance=exit_meeting)
    return render(request, 'audit_reporting/exit_meeting.html', {'form': form})



# Delete exit_meeting
def delete_exit_meeting(request, meeting_id):
    exit_meeting = get_object_or_404(ExitMeeting, meeting_id=meeting_id) 
    exit_meeting.delete()
    messages.success(request, "Exit Meeting deleted successfully!")
    return redirect('list_exit_meeting')


####
def list_draft_report(request):
    # Get all records by default
    draft_reports = DraftReport.objects.all()
    form = DraftReportForm()

    
    # Default sorting by report_id
    sort_by = request.GET.get('sort_by', 'report_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        draft_reports = draft_reports.order_by(sort_by)
    else:
        draft_reports = draft_reports.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(draft_reports, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_draft_reports = paginator.page(page)
    except PageNotAnInteger:
        paginated_draft_reports = paginator.page(1)
    except EmptyPage:
        paginated_draft_reports = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Draft Report",
        'draft_reports':draft_reports, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_draft_reports': paginated_draft_reports,
        'rows_per_page': rows_per_page,
        'form': form,
        'drafted_by_choices': Staff.objects.all(),
    }
    return render(request, 'audit_reporting/draft_report.html', context)


# Add Oversigh 

def add_draft_report(request):
    form = DraftReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Draft Report added successfully!")
            return redirect('list_draft_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Draft Report. Please correct the errors.")
    return redirect('list_draft_report')

# DraftReport 
def edit_draft_report(request, report_id):
    draft_report = get_object_or_404(DraftReport, report_id=report_id)
    if request.method == 'POST':
        form = DraftReportForm(request.POST, instance=draft_report)
        if form.is_valid():
            form.save()
            messages.success(request, "Draft Report updated successfully!")
            return redirect('list_draft_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Draft Report. Please correct the errors.")
    else:
        form = DraftReportForm(instance=draft_report)
    return render(request, 'audit_reporting/draft_report.html', {'form': form})



# Delete draft_report
def delete_draft_report(request, report_id):
    draft_report = get_object_or_404(DraftReport, report_id=report_id) 
    draft_report.delete()
    messages.success(request, "Draft Report deleted successfully!")
    return redirect('list_draft_report')

####
def list_final_report(request):
    # Get all records by default
    final_reports = FinalReport.objects.all()
    form = FinalReportForm()

    
    # Default sorting by report_id
    sort_by = request.GET.get('sort_by', 'report_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        final_reports = final_reports.order_by(sort_by)
    else:
        final_reports = final_reports.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(final_reports, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_final_reports = paginator.page(page)
    except PageNotAnInteger:
        paginated_final_reports = paginator.page(1)
    except EmptyPage:
        paginated_final_reports = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Final Report",
        'final_reports':final_reports, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_final_reports': paginated_final_reports,
        'rows_per_page': rows_per_page,
        'form': form,
        'approved_by_choices': Staff.objects.all(),
    }
    return render(request, 'audit_reporting/final_report.html', context)


# Add Oversigh 

def add_final_report(request):
    form = FinalReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Final Report added successfully!")
            return redirect('list_final_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Final Report. Please correct the errors.")
    return redirect('list_final_report')

# FinalReport 
def edit_final_report(request, report_id):
    final_report = get_object_or_404(FinalReport, report_id=report_id)
    if request.method == 'POST':
        form = FinalReportForm(request.POST, instance=final_report)
        if form.is_valid():
            form.save()
            messages.success(request, "Final Report updated successfully!")
            return redirect('list_final_report')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Final Report. Please correct the errors.")
    else:
        form = FinalReportForm(instance=final_report)
    return render(request, 'audit_reporting/final_report.html', {'form': form})



# Delete final_report
def delete_final_report(request, report_id):
    final_report = get_object_or_404(FinalReport, report_id=report_id) 
    final_report.delete()
    messages.success(request, "Final Report deleted successfully!")
    return redirect('list_final_report')


####
def list_feedback(request):
    # Get all records by default
    feedbacks = Feedback.objects.all()
    form = FeedbackForm()

    
    # Default sorting by survey_id
    sort_by = request.GET.get('sort_by', 'survey_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        feedbacks = feedbacks.order_by(sort_by)
    else:
        feedbacks = feedbacks.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(feedbacks, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_feedbacks = paginator.page(page)
    except PageNotAnInteger:
        paginated_feedbacks = paginator.page(1)
    except EmptyPage:
        paginated_feedbacks = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Feedback",
        'feedbacks':feedbacks, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_feedbacks': paginated_feedbacks,
        'rows_per_page': rows_per_page,
        'form': form,
        'auditee_name_choices': Staff.objects.all(),
    }
    return render(request, 'iam/feedback.html', context)


# Add Oversigh 

def add_feedback(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback added successfully!")
            return redirect('list_feedback')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Feedback. Please correct the errors.")
    return redirect('list_feedback')

# Feedback 
def edit_feedback(request, survey_id):
    feedback = get_object_or_404(Feedback, survey_id=survey_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback updated successfully!")
            return redirect('list_feedback')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Feedback. Please correct the errors.")
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'iam/feedback.html', {'form': form})



# Delete feedback
def delete_feedback(request, survey_id):
    feedback = get_object_or_404(Feedback, survey_id=survey_id) 
    feedback.delete()
    messages.success(request, "Feedback deleted successfully!")
    return redirect('list_feedback')

####
def list_follow_up(request):
    # Get all records by default
    follow_ups = AuditFollowUp.objects.all()
    form = AuditFollowUpForm()

    
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
        'page_title': "Audit FollowUp",
        'follow_ups':follow_ups, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_follow_ups': paginated_follow_ups,
        'rows_per_page': rows_per_page,
        'form': form,
        'follow_up_by_choices': Staff.objects.all(),
    }
    return render(request, 'iam/follow_up.html', context)


# Add Oversigh 

def add_follow_up(request):
    form = AuditFollowUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "AuditFollowUp added successfully!")
            return redirect('list_follow_up')
        else:
            print(form.errors)
            messages.error(request, "Failed to add AuditFollowUp. Please correct the errors.")
    return redirect('list_follow_up')

# AuditFollowUp 
def edit_follow_up(request, follow_up_id):
    follow_up = get_object_or_404(AuditFollowUp, follow_up_id=follow_up_id)
    if request.method == 'POST':
        form = AuditFollowUpForm(request.POST, instance=follow_up)
        if form.is_valid():
            form.save()
            messages.success(request, "AuditFollowUp updated successfully!")
            return redirect('list_follow_up')
        else:
            print(form.errors)
            messages.error(request, "Failed to update AuditFollowUp. Please correct the errors.")
    else:
        form = AuditFollowUpForm(instance=follow_up)
    return render(request, 'iam/follow_up.html', {'form': form})



# Delete follow_up
def delete_follow_up(request, follow_up_id):
    follow_up = get_object_or_404(AuditFollowUp, follow_up_id=follow_up_id) 
    follow_up.delete()
    messages.success(request, "AuditFollowUp deleted successfully!")
    return redirect('list_follow_up')
