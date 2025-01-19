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
from django.db.models import Sum,Count
# Create your views here.
# IAM Dashboard View
def dashboard(request):

    # Aggregate inherent and residual risks by category
    category_totals = RiskAssessment.objects.values('risk_type').annotate(
        total_inherent_risk=Sum('inherent_risk'),
        total_residual_risk=Sum('residual_risk')
    )

    # Format data for the chart
    category_chart_data = {
        'categories': [cat['risk_type'] for cat in category_totals],
        'inherent_risks': [cat['total_inherent_risk'] or 0 for cat in category_totals],
        'residual_risks': [cat['total_residual_risk'] or 0 for cat in category_totals],
    }

    risk_score_data = AuditUniverse.objects.values('risk_score').annotate(count=Count('audit_id'))

    # Format data for ECharts
    risk_chart_data = {
        'risk_scores': [item['risk_score'] for item in risk_score_data],
        'counts': [item['count'] for item in risk_score_data]
    }
    entity_type_data = AuditUniverse.objects.values('entity_type').annotate(count=Count('audit_id'))

    entity_type_chart_data = {
        'entity_types': [item['entity_type'] for item in entity_type_data],
        'counts': [item['count'] for item in entity_type_data]
    }


    context = {
        'page_title': "IAM Dashboard",
        'category_chart_data': category_chart_data,
        'risk_chart_data': risk_chart_data, 
        'entity_type_chart_data': entity_type_chart_data, 
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


def audit_testing_dashboard(request):
    components = [
        {"name": "Audit Test", "icon": "fas fa-file-alt", "link": "audit_tests"},  # File for reporting
        {"name": "Working Paper", "icon": "fas fa-chart-line", "link": "working_papers"},  # Chart line for trends report
    ]
    context = {
        'page_title': "Audit Testing",
        'components': components,
    }
    return render(request, 'audit_testing/dashboard.html', context)


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
        'entity_type_choices': AuditUniverse._meta.get_field('entity_type').choices,
        'strategic_relevance_choices': AuditUniverse._meta.get_field('strategic_relevance').choices,
        'location_category_choices': AuditUniverse._meta.get_field('location_category').choices,
        'process_category_choices': AuditUniverse._meta.get_field('process_category').choices,
        'organizational_category_choices': AuditUniverse._meta.get_field('organizational_category').choices,
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
        'control_effectiveness_choices': RiskAssessment._meta.get_field('control_effectiveness').choices,
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

#
def risk_control_matrix(request):
    processes = ProcessUnderstanding.objects.all()
    context = {
        'processes': processes
    }
    return render(request, 'micro_planning/risk_control_matrix.html', context)

######
def list_process_understanding(request):
    # Get all records by default
    process_understandings = ProcessUnderstanding.objects.all()
    form = ProcessUnderstandingForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        process_understandings = process_understandings.order_by(sort_by)
    else:
        process_understandings = process_understandings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(process_understandings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_process_understandings = paginator.page(page)
    except PageNotAnInteger:
        paginated_process_understandings = paginator.page(1)
    except EmptyPage:
        paginated_process_understandings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Process Understanding",
        'process_understandings':process_understandings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_process_understandings': paginated_process_understandings,
        'rows_per_page': rows_per_page,
        'form': form,
    }
    return render(request, 'micro_planning/risk_control_matrix/process_understanding.html', context)


# Add Oversigh 

def add_process_understanding(request):
    form = ProcessUnderstandingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Process Understanding added successfully!")
            return redirect('list_process_understanding')
        else:
            print(form.errors)
            messages.error(request, "Failed to add ProcessUnderstanding. Please correct the errors.")
    return redirect('list_process_understanding')

# ProcessUnderstanding 
def edit_process_understanding(request, id):
    process_understanding = get_object_or_404(ProcessUnderstanding, id=id)
    if request.method == 'POST':
        form = ProcessUnderstandingForm(request.POST, instance=process_understanding)
        if form.is_valid():
            form.save()
            messages.success(request, "Process Understanding updated successfully!")
            return redirect('list_process_understanding')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Process Understanding. Please correct the errors.")
    else:
        form = ProcessUnderstandingForm(instance=process_understanding)
    return render(request, 'micro_planning/risk_control_matrix/process_understanding.html', {'form': form})



# Delete process_understanding
def delete_process_understanding(request, id):
    process_understanding = get_object_or_404(ProcessUnderstanding, id=id) 
    process_understanding.delete()
    messages.success(request, "Process Understanding deleted successfully!")
    return redirect('list_process_understanding')

def list_sub_process(request):
    # Get all records by default
    sub_processs = SubProcess.objects.all()
    form = SubProcessForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        sub_processs = sub_processs.order_by(sort_by)
    else:
        sub_processs = sub_processs.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(sub_processs, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_sub_processs = paginator.page(page)
    except PageNotAnInteger:
        paginated_sub_processs = paginator.page(1)
    except EmptyPage:
        paginated_sub_processs = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "SubProcess",
        'sub_processs':sub_processs, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_sub_processs': paginated_sub_processs,
        'rows_per_page': rows_per_page,
        'form': form,
        'process_choices': ProcessUnderstanding.objects.all(),
    }
    return render(request, 'micro_planning/risk_control_matrix/sub_process.html', context)

#

# Add Oversigh 

def add_sub_process(request):
    form = SubProcessForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "SubProcess added successfully!")
            return redirect('list_sub_process')
        else:
            print(form.errors)
            messages.error(request, "Failed to add SubProcess. Please correct the errors.")
    return redirect('list_sub_process')

# SubProcess 
def edit_sub_process(request, id):
    sub_process = get_object_or_404(SubProcess, id=id)
    if request.method == 'POST':
        form = SubProcessForm(request.POST, instance=sub_process)
        if form.is_valid():
            form.save()
            messages.success(request, "SubProcess updated successfully!")
            return redirect('list_sub_process')
        else:
            print(form.errors)
            messages.error(request, "Failed to update SubProcess. Please correct the errors.")
    else:
        form = SubProcessForm(instance=sub_process)
    return render(request, 'micro_planning/risk_control_matrix/sub_process.html', {'form': form})


# Delete sub_process
def delete_sub_process(request, id):
    sub_process = get_object_or_404(SubProcess, id=id) 
    sub_process.delete()
    messages.success(request, "SubProcess deleted successfully!")
    return redirect('list_sub_process')

def list_activity(request):
    # Get all records by default
    activitys = Activity.objects.all()
    form = ActivityForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        activitys = activitys.order_by(sort_by)
    else:
        activitys = activitys.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(activitys, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_activitys = paginator.page(page)
    except PageNotAnInteger:
        paginated_activitys = paginator.page(1)
    except EmptyPage:
        paginated_activitys = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Activity",
        'activitys':activitys, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_activitys': paginated_activitys,
        'rows_per_page': rows_per_page,
        'form': form,
        'sub_process_choices': SubProcess.objects.all(),
    }
    return render(request, 'micro_planning/risk_control_matrix/activity.html', context)

#

# Add Oversigh 

def add_activity(request):
    form = ActivityForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Activity added successfully!")
            return redirect('list_activity')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Activity. Please correct the errors.")
    return redirect('list_activity')

# Activity 
def edit_activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated successfully!")
            return redirect('list_activity')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Activity. Please correct the errors.")
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'micro_planning/risk_control_matrix/activity.html', {'form': form})


# Delete activity
def delete_activity(request, id):
    activity = get_object_or_404(Activity, id=id) 
    activity.delete()
    messages.success(request, "Activity deleted successfully!")
    return redirect('list_activity')

def list_process_risk(request):
    # Get all records by default
    process_risks = ProcessRisk.objects.all()
    form = ProcessRiskForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        process_risks = process_risks.order_by(sort_by)
    else:
        process_risks = process_risks.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(process_risks, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_process_risks = paginator.page(page)
    except PageNotAnInteger:
        paginated_process_risks = paginator.page(1)
    except EmptyPage:
        paginated_process_risks = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Controls",
        'process_risks':process_risks, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_process_risks': paginated_process_risks,
        'rows_per_page': rows_per_page,
        'form': form,
        'risk_type_choices': ProcessRisk._meta.get_field('risk_type').choices,
        'sub_process_choices': SubProcess.objects.all(),
    }
    return render(request, 'micro_planning/risk_control_matrix/process_risk.html', context)


# Add Oversigh 

def add_process_risk(request):
    form = ProcessRiskForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "ProcessRisk added successfully!")
            return redirect('list_process_risk')
        else:
            print(form.errors)
            messages.error(request, "Failed to add ProcessRisk. Please correct the errors.")
    return redirect('list_process_risk')

# ProcessRisk 
def edit_process_risk(request, id):
    process_risk = get_object_or_404(ProcessRisk, id=id)
    if request.method == 'POST':
        form = ProcessRiskForm(request.POST, instance=process_risk)
        if form.is_valid():
            form.save()
            messages.success(request, "ProcessRisk updated successfully!")
            return redirect('list_process_risk')
        else:
            print(form.errors)
            messages.error(request, "Failed to update ProcessRisk. Please correct the errors.")
    else:
        form = ProcessRiskForm(instance=process_risk)
    return render(request, 'micro_planning/risk_control_matrix/process_risk.html', {'form': form})


# Delete process_risk
def delete_process_risk(request, id):
    process_risk = get_object_or_404(ProcessRisk, id=id) 
    process_risk.delete()
    messages.success(request, "ProcessRisk deleted successfully!")
    return redirect('list_process_risk')

def list_control(request):
    # Get all records by default
    controls = control.objects.all()
    form = ControlForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        controls = controls.order_by(sort_by)
    else:
        controls = controls.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(controls, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_controls = paginator.page(page)
    except PageNotAnInteger:
        paginated_controls = paginator.page(1)
    except EmptyPage:
        paginated_controls = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Controls",
        'controls':controls, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_controls': paginated_controls,
        'rows_per_page': rows_per_page,
        'form': form,
        'control_type_choices': control._meta.get_field('control_type').choices,
        'control_class_choices': control._meta.get_field('control_class').choices,
        'sub_process_choices': SubProcess.objects.all(),
        'performed_by_choices': Staff.objects.all(),
    }
    return render(request, 'micro_planning/risk_control_matrix/control.html', context)


# Add Oversigh 

def add_control(request):
    form = ControlForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "control added successfully!")
            return redirect('list_control')
        else:
            print(form.errors)
            messages.error(request, "Failed to add control. Please correct the errors.")
    return redirect('list_control')

# control 
def edit_control(request, id):
    controls = get_object_or_404(control, id=id)
    
    if request.method == 'POST':
        form = ControlForm(request.POST, instance=controls)
        if form.is_valid():
            form.save()
            messages.success(request, "control updated successfully!")
            return redirect('list_control')
        else:
            print(form.errors)
            messages.error(request, "Failed to update control. Please correct the errors.")
    else:
        form = ControlForm(instance=controls)
    return render(request, 'micro_planning/risk_control_matrix/control.html', {'form': form})


# Delete control
def delete_control(request, id):
    controls = get_object_or_404(control, id=id) 
    controls.delete()
    messages.success(request, "control deleted successfully!")
    return redirect('list_control')

#######


def process_overview(request):
    rows = []
    process_count = 1  # Start the process sequence from 1

    processes = ProcessUnderstanding.objects.all()

    for process in processes:
        subprocesses = SubProcess.objects.filter(process_id=process)

        if not subprocesses.exists():
            # If no subprocesses, still create a blank row for the process
            rows.append({
                'process_id': str(process_count),
                'process_name': process.name,
                'process_description': process.description,
                'subprocess_id': '',
                'subprocess_name': '',
                'subprocess_description': '',
                'activity_id': '',
                'activity_name': '',
                'activity_description': '',
                'risk_id': '',
                'risk_name': '',
                'risk_description': '',
                'risk_score': '',
                'risk_type': '',
                'control_id': '',
                'control_name': '',
                'control_description': '',
                'control_objective': '',
                'control_performed_by': '',
                'control_performed_date': '',
                'control_location': '',
                'control_class': '',
                'control_type': '',
                'control_final_decision': '',
            })

        subprocess_count = 1  # Subprocess sequence starts for each process
        for subprocess in subprocesses:
            activity_count = 1
            control_count = 1
            risk_count = 1

            activities = Activity.objects.filter(subprocess_id=subprocess)
            risks = ProcessRisk.objects.filter(subprocess_id=subprocess)
            controls = control.objects.filter(subprocess_id=subprocess)

            max_rows = max(len(activities), len(risks), len(controls), 1)

            for i in range(max_rows):
                row = {
                    'process_id': str(process_count),
                    'process_name': process.name,
                    'process_description': process.description,
                    'subprocess_id': f"{process_count}.{subprocess_count}",
                    'subprocess_name': subprocess.name,
                    'subprocess_description': subprocess.description,
                    'activity_id': '',
                    'activity_name': '',
                    'activity_description': '',
                    'risk_id': '',
                    'risk_name': '',
                    'risk_description': '',
                    'risk_score': '',
                    'risk_type': '',
                    'control_id': '',
                    'control_name': '',
                    'control_description': '',
                    'control_objective': '',
                    'control_performed_by': '',
                    'control_performed_date': '',
                    'control_location': '',
                    'control_class': '',
                    'control_type': '',
                    'control_final_decision': '',
                }

                # Add activity data
                if i < len(activities):
                    activity = activities[i]
                    row['activity_id'] = f"{process_count}.{subprocess_count}.{activity_count}"
                    row['activity_name'] = activity.name
                    row['activity_description'] = activity.description
                    activity_count += 1

                # Add risk data
                if i < len(risks):
                    risk = risks[i]
                    row['risk_id'] = f"{process_count}.{subprocess_count}.{risk_count}"
                    row['risk_name'] = risk.name
                    row['risk_description'] = risk.description
                    row['risk_score'] = risk.risk_score
                    row['risk_type'] = risk.risk_type
                    risk_count += 1

                # Add control data
                if i < len(controls):
                    ctrl = controls[i]
                    row['control_id'] = f"{process_count}.{subprocess_count}.{control_count}"
                    row['control_name'] = ctrl.name
                    row['control_description'] = ctrl.description
                    row['control_objective'] = ctrl.objective
                    row['control_performed_by'] = ctrl.performed_by
                    row['control_performed_date'] = ctrl.performed_date
                    row['control_location'] = ctrl.control_location
                    row['control_class'] = ctrl.control_class
                    row['control_type'] = ctrl.control_type
                    row['control_final_decision'] = ctrl.final_decision
                    control_count += 1

                rows.append(row)

            subprocess_count += 1  # Increment subprocess sequence

        process_count += 1  # Increment process sequence

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(rows, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_rows = paginator.page(page)
    except PageNotAnInteger:
        paginated_rows = paginator.page(1)
    except EmptyPage:
        paginated_rows = paginator.page(paginator.num_pages)

    return render(request, 'micro_planning/risk_control_matrix.html', {
        'paginated_rows': paginated_rows,
        'rows_per_page': rows_per_page,
        'request': request,
        'page_title':"RCM"
    })


def export_process_overview_to_excel(request):
    rows = []
    process_count = 1  # Start the process sequence from 1

    processes = ProcessUnderstanding.objects.all()

    for process in processes:
        subprocesses = SubProcess.objects.filter(process_id=process)

        if not subprocesses.exists():
            rows.append({
                'Process ID': str(process_count),
                'Process Name': process.name,
                'Process Description': process.description,
                'Subprocess ID': '',
                'Subprocess Name': '',
                'Subprocess Description': '',
                'Activity ID': '',
                'Activity Name': '',
                'Activity Description': '',
                'Risk ID': '',
                'Risk Name': '',
                'Risk Description': '',
                'Risk Score': '',
                'Risk Type': '',
                'Control ID': '',
                'Control Name': '',
                'Control Description': '',
                'Control Objective': '',
                'Control Performed By': '',
                'Control Performed Date': '',
                'Control Location': '',
                'Control Class': '',
                'Control Type': '',
                'Control Final Decision': '',
            })

        subprocess_count = 1  # Subprocess sequence starts for each process
        for subprocess in subprocesses:
            activity_count = 1
            control_count = 1
            risk_count = 1

            activities = Activity.objects.filter(subprocess_id=subprocess)
            risks = ProcessRisk.objects.filter(subprocess_id=subprocess)
            controls = control.objects.filter(subprocess_id=subprocess)

            max_rows = max(len(activities), len(risks), len(controls), 1)

            for i in range(max_rows):
                row = {
                    'Process ID': str(process_count),
                    'Process Name': process.name,
                    'Process Description': process.description,
                    'Subprocess ID': f"{process_count}.{subprocess_count}",
                    'Subprocess Name': subprocess.name,
                    'Subprocess Description': subprocess.description,
                    'Activity ID': '',
                    'Activity Name': '',
                    'Activity Description': '',
                    'Risk ID': '',
                    'Risk Name': '',
                    'Risk Description': '',
                    'Risk Score': '',
                    'Risk Type': '',
                    'Control ID': '',
                    'Control Name': '',
                    'Control Description': '',
                    'Control Objective': '',
                    'Control Performed By': '',
                    'Control Performed Date': '',
                    'Control Location': '',
                    'Control Class': '',
                    'Control Type': '',
                    'Control Final Decision': '',
                }

                # Add activity data
                if i < len(activities):
                    activity = activities[i]
                    row['Activity ID'] = f"{process_count}.{subprocess_count}.{activity_count}"
                    row['Activity Name'] = activity.name
                    row['Activity Description'] = activity.description
                    activity_count += 1

                # Add risk data
                if i < len(risks):
                    risk = risks[i]
                    row['Risk ID'] = f"{process_count}.{subprocess_count}.{risk_count}"
                    row['Risk Name'] = risk.name
                    row['Risk Description'] = risk.description
                    row['Risk Score'] = risk.risk_score
                    row['Risk Type'] = risk.risk_type
                    risk_count += 1

                # Add control data
                if i < len(controls):
                    ctrl = controls[i]
                    row['Control ID'] = f"{process_count}.{subprocess_count}.{control_count}"
                    row['Control Name'] = ctrl.name
                    row['Control Description'] = ctrl.description
                    row['Control Objective'] = ctrl.objective
                    row['Control Performed By'] = ctrl.performed_by
                    row['Control Performed Date'] = ctrl.performed_date
                    row['Control Location'] = ctrl.control_location
                    row['Control Class'] = ctrl.control_class
                    row['Control Type'] = ctrl.control_type
                    row['Control Final Decision'] = ctrl.final_decision
                    control_count += 1

                rows.append(row)

            subprocess_count += 1  # Increment subprocess sequence

        process_count += 1  # Increment process sequence

    # Create a DataFrame from rows
    df = pd.DataFrame(rows)

    # Generate the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Risk And Control Matrix.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Risk And Control Matrix')

    return response

######
def list_audit_test(request):
    # Get all records by default
    audit_tests = AuditTest.objects.all()
    form = AuditTestForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_tests = audit_tests.order_by(sort_by)
    else:
        audit_tests = audit_tests.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_tests, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_tests = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_tests = paginator.page(1)
    except EmptyPage:
        paginated_audit_tests = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Test",
        'audit_tests':audit_tests, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_tests': paginated_audit_tests,
        'rows_per_page': rows_per_page,
        'form': form,
        'tested_by_choices': Staff.objects.all(),
        'sub_process_choices': SubProcess.objects.all(),
        'status_choices': AuditTest._meta.get_field('status').choices,
    }
    return render(request, 'micro_planning/audit_program/audit_test.html', context)


# Add Oversigh 

def add_audit_test(request):
    form = AuditTestForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Test added successfully!")
            return redirect('list_audit_test')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Test. Please correct the errors.")
    return redirect('list_audit_test')

# Audit Test 
def edit_audit_test(request, id):
    audit_test = get_object_or_404(AuditTest, id=id)
    if request.method == 'POST':
        form = AuditTestForm(request.POST, instance=audit_test)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Test updated successfully!")
            return redirect('list_audit_test')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Test. Please correct the errors.")
    else:
        form = AuditTestForm(instance=audit_test)
    return render(request, 'micro_planning/audit_program/audit_test.html', {'form': form})



# Delete audit_test
def delete_audit_test(request, id):
    audit_test = get_object_or_404(AuditTest, id=id) 
    audit_test.delete()
    messages.success(request, "Audit Procedure deleted successfully!")
    return redirect('list_audit_test')

def list_audit_procedure(request):
    # Get all records by default
    audit_procedures = AuditProcedure.objects.all()
    form = AuditProcedureForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        audit_procedures = audit_procedures.order_by(sort_by)
    else:
        audit_procedures = audit_procedures.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(audit_procedures, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_audit_procedures = paginator.page(page)
    except PageNotAnInteger:
        paginated_audit_procedures = paginator.page(1)
    except EmptyPage:
        paginated_audit_procedures = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Audit Procedure",
        'audit_procedures':audit_procedures, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_audit_procedures': paginated_audit_procedures,
        'rows_per_page': rows_per_page,
        'form': form,
        'conducted_by_choices': Staff.objects.all(),
        'sub_process_choices': SubProcess.objects.all(),
    }
    return render(request, 'micro_planning/audit_program/audit_procedure.html', context)


# Add Oversigh 

def add_audit_procedure(request):
    form = AuditProcedureForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Procedure added successfully!")
            return redirect('list_audit_procedure')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Audit Procedure. Please correct the errors.")
    return redirect('list_audit_procedure')

# Audit Procedure 
def edit_audit_procedure(request, id):
    audit_procedure = get_object_or_404(AuditProcedure, id=id)
    if request.method == 'POST':
        form = AuditProcedureForm(request.POST, instance=audit_procedure)
        if form.is_valid():
            form.save()
            messages.success(request, "Audit Procedure updated successfully!")
            return redirect('list_audit_procedure')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Audit Procedure. Please correct the errors.")
    else:
        form = AuditProcedureForm(instance=audit_procedure)
    return render(request, 'micro_planning/audit_program/audit_procedure.html', {'form': form})



# Delete audit_procedure
def delete_audit_procedure(request, id):
    audit_procedure = get_object_or_404(AuditProcedure, id=id) 
    audit_procedure.delete()
    messages.success(request, "Audit Procedure deleted successfully!")
    return redirect('list_audit_procedure')


def list_requirements_list(request):
    # Get all records by default
    requirements_lists = RequirementsList.objects.all()
    form = RequirementsListForm()

    
    # Default sorting by id
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        requirements_lists = requirements_lists.order_by(sort_by)
    else:
        requirements_lists = requirements_lists.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(requirements_lists, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_requirements_lists = paginator.page(page)
    except PageNotAnInteger:
        paginated_requirements_lists = paginator.page(1)
    except EmptyPage:
        paginated_requirements_lists = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "List of Requirements",
        'requirements_lists':requirements_lists, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_requirements_lists': paginated_requirements_lists,
        'rows_per_page': rows_per_page,
        'form': form,
        'requested_by_choices': Staff.objects.all(),
        'escalation_to_choices': Staff.objects.all(),
        'test_id_choices': AuditTest.objects.all(),
        'status_choices': RequirementsList._meta.get_field('status').choices,
    }
    return render(request, 'micro_planning/audit_program/requirements_list.html', context)


# Add Oversigh 

def add_requirements_list(request):
    form = RequirementsListForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Requirements added successfully!")
            return redirect('list_requirements_list')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Requirements. Please correct the errors.")
    return redirect('list_requirements_list')

# Requirements List 
def edit_requirements_list(request, id):
    requirements_list = get_object_or_404(RequirementsList, id=id)
    if request.method == 'POST':
        form = RequirementsListForm(request.POST, instance=requirements_list)
        if form.is_valid():
            form.save()
            messages.success(request, "Requirements updated successfully!")
            return redirect('list_requirements_list')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Requirements. Please correct the errors.")
    else:
        form = RequirementsListForm(instance=requirements_list)
    return render(request, 'micro_planning/audit_program/requirements_list.html', {'form': form})



# Delete requirements_list
def delete_requirements_list(request, id):
    requirements_list = get_object_or_404(RequirementsList, id=id) 
    requirements_list.delete()
    messages.success(request, "Requirements deleted successfully!")
    return redirect('list_requirements_list')



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def audit_program_overview(request):
    rows = []
    subprocess_count = 1  # Start the subprocess sequence from 1

    subprocesses = SubProcess.objects.all()

    for subprocess in subprocesses:
        audit_tests = AuditTest.objects.filter(subprocess_id=subprocess)

        # If no audit tests, still create a blank row for the subprocess
        if not audit_tests.exists():
            rows.append({
                'subprocess_id': str(subprocess_count),
                'subprocess_name': subprocess.name,
                'subprocess_description': subprocess.description,
                'audit_test_id': '',
                'audit_test_name': '',
                'audit_test_description': '',
                'procedure_id': '',
                'procedure_name': '',
                'procedure_description': '',
                'requirements_list_id': '',
                'requirements_name': '',
                'requirements_description': '',
                'requested_by': '',
                'requested_from': '',
                'requested_date': '',
                'date_received': '',
                'status': '',
            })

        audit_test_count = 1  # Start the audit test sequence for each subprocess
        for audit_test in audit_tests:
            procedures = AuditProcedure.objects.filter(subprocess_id=subprocess)
            requirements = RequirementsList.objects.filter(test_id=audit_test)

            max_rows = max(len(procedures), len(requirements), 1)

            for i in range(max_rows):
                row = {
                    'subprocess_id': f"{subprocess_count}",
                    'subprocess_name': subprocess.name,
                    'subprocess_description': subprocess.description,
                    'audit_test_id': f"{subprocess_count}.{audit_test_count}",
                    'audit_test_name': audit_test.name,
                    'audit_test_description': audit_test.description,
                    'procedure_id': '',
                    'procedure_name': '',
                    'procedure_description': '',
                    'requirements_list_id': '',
                    'requirements_name': '',
                    'requirements_description': '',
                    'requested_by': '',
                    'requested_from': '',
                    'requested_date': '',
                    'date_received': '',
                    'status': '',
                }

                # Add procedure data
                if i < len(procedures):
                    procedure = procedures[i]
                    row['procedure_id'] = f"{subprocess_count}.{audit_test_count}.{i + 1}"
                    row['procedure_name'] = procedure.name
                    row['procedure_description'] = procedure.description

                # Add requirements data
                if i < len(requirements):
                    requirement = requirements[i]
                    row['requirements_list_id'] = f"{subprocess_count}.{audit_test_count}.{i + 1}"
                    row['requirements_name'] = requirement.name
                    row['requirements_description'] = requirement.Description
                    row['requested_by'] = requirement.requested_by if requirement.requested_by else ''
                    row['requested_from'] = requirement.requested_from
                    row['requested_date'] = requirement.date_requested
                    row['date_received'] = requirement.date_received
                    row['status'] = requirement.status

                rows.append(row)

            audit_test_count += 1  # Increment the audit test sequence

        subprocess_count += 1  # Increment the subprocess sequence

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(rows, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_rows = paginator.page(page)
    except PageNotAnInteger:
        paginated_rows = paginator.page(1)
    except EmptyPage:
        paginated_rows = paginator.page(paginator.num_pages)

    return render(request, 'micro_planning/audit_program.html', {
        'paginated_rows': paginated_rows,
        'rows_per_page': rows_per_page,
        'request': request,
        'page_title':"Audit Program",
    })



def export_audit_program_overview_to_excel(request):
    rows = []
    subprocess_count = 1  # Start the subprocess sequence from 1

    subprocesses = SubProcess.objects.all()

    for subprocess in subprocesses:
        audit_tests = AuditTest.objects.filter(subprocess_id=subprocess)

        # If no audit tests, still create a blank row for the subprocess
        if not audit_tests.exists():
            rows.append({
                'Subprocess ID': str(subprocess_count),
                'Subprocess Name': subprocess.name,
                'Subprocess Description': subprocess.description,
                'Audit Test ID': '',
                'Audit Test Name': '',
                'Audit Test Description': '',
                'Procedure ID': '',
                'Procedure Name': '',
                'Procedure Description': '',
                'Requirements List ID': '',
                'Requirements Name': '',
                'Requirements Description': '',
                'Requested By': '',
                'Requested From': '',
                'Requested Date': '',
                'Date Received': '',
                'Status': '',
            })

        audit_test_count = 1  # Start the audit test sequence for each subprocess
        for audit_test in audit_tests:
            procedures = AuditProcedure.objects.filter(subprocess_id=subprocess)
            requirements = RequirementsList.objects.filter(test_id=audit_test)

            max_rows = max(len(procedures), len(requirements), 1)

            for i in range(max_rows):
                row = {
                    'Subprocess ID': f"{subprocess_count}",
                    'Subprocess Name': subprocess.name,
                    'Subprocess Description': subprocess.description,
                    'Audit Test ID': f"{subprocess_count}.{audit_test_count}",
                    'Audit Test Name': audit_test.name,
                    'Audit Test Description': audit_test.description,
                    'Procedure ID': '',
                    'Procedure Name': '',
                    'Procedure Description': '',
                    'Requirements List ID': '',
                    'Requirements Name': '',
                    'Requirements Description': '',
                    'Requested By': '',
                    'Requested From': '',
                    'Requested Date': '',
                    'Date Received': '',
                    'Status': '',
                }

                # Add procedure data
                if i < len(procedures):
                    procedure = procedures[i]
                    row['Procedure ID'] = f"{subprocess_count}.{audit_test_count}.{i + 1}"
                    row['Procedure Name'] = procedure.name
                    row['Procedure Description'] = procedure.description

                # Add requirements data
                if i < len(requirements):
                    requirement = requirements[i]
                    row['Requirements List ID'] = f"{subprocess_count}.{audit_test_count}.{i + 1}"
                    row['Requirements Name'] = requirement.name
                    row['Requirements Description'] = requirement.Description
                    row['Requested By'] = requirement.requested_by.name if requirement.requested_by else ''
                    row['Requested From'] = requirement.requested_from
                    row['Requested Date'] = requirement.date_requested
                    row['Date Received'] = requirement.date_received
                    row['Status'] = requirement.status

                rows.append(row)

            audit_test_count += 1  # Increment the audit test sequence

        subprocess_count += 1  # Increment the subprocess sequence

    # Create a DataFrame from rows
    df = pd.DataFrame(rows)

    # Generate the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=audit_program_overview.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Audit Program Overview')

    return response

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
