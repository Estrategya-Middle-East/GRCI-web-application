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
# BCM Dashboard View
def dashboard(request):
    components = [
        {"name": "Governance and Leadership", "icon": "fas fa-gavel", "link": "bcm_governances"},  # Governance and oversight
        {"name": "Business Impact Analysis", "icon": "fas fa-chart-pie", "link": "business_impact_analysiss"},  # Chart for impact analysis
        {"name": "Risk Assessment and Management", "icon": "fas fa-tasks", "link": "continuity_risk_assessments"},  # Tasks for risk management
        {"name": "Strategy Development", "icon": "fas fa-lightbulb", "link": "continuity_strategys"},  # Lightbulb for strategy
        {"name": "Plan Development and Implementation", "icon": "fas fa-cogs", "link": "business_continuity_plans"},  # Cog for development and implementation
        {"name": "Testing and Exercises", "icon": "fas fa-vial", "link": "continuity_testings"},  # Test tube for testing exercises
        {"name": "Incident Response and Activation", "icon": "fas fa-bell", "link": "incident_activations"},  # Bell for alerts or incidents
        {"name": "Crisis Communication", "icon": "fas fa-comments", "link": "crisis_communications"},  # Comments for communication
        {"name": "Program Monitoring and Review", "icon": "fas fa-eye", "link": "bcm_program_reviews"},  # Eye for monitoring
        #{"name": "Document Management", "icon": "fas fa-folder-open", "link": "#"},  # Folder for document management
    ]
    context = {
        'page_title': "BCM Dashboard",
        'components': components,
    }
    return render(request, 'bcm/dashboard.html', context)

######
def list_bcm_governance(request):
    # Get all records by default
    bcm_governances = BCMGovernance.objects.all()
    form = BCMGovernanceForm()

    
    # Default sorting by governance_id
    sort_by = request.GET.get('sort_by', 'governance_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        bcm_governances = bcm_governances.order_by(sort_by)
    else:
        bcm_governances = bcm_governances.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(bcm_governances, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_bcm_governances = paginator.page(page)
    except PageNotAnInteger:
        paginated_bcm_governances = paginator.page(1)
    except EmptyPage:
        paginated_bcm_governances = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "BCM Governance",
        'bcm_governances':bcm_governances, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_bcm_governances': paginated_bcm_governances,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': BCMGovernance._meta.get_field('approval_status').choices,
        'review_frequency_choices': BCMGovernance._meta.get_field('review_frequency').choices,
        'governance_owner_choices': Staff.objects.all(),
        'approver_id_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/bcm_governance.html', context)


# Add Oversigh 

def add_bcm_governance(request):
    form = BCMGovernanceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Governance added successfully!")
            return redirect('list_bcm_governance')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Governance. Please correct the errors.")
    return redirect('list_bcm_governance')

# BCMGovernance Dashboard
def edit_bcm_governance(request, governance_id):
    bcm_governance = get_object_or_404(BCMGovernance, governance_id=governance_id)
    if request.method == 'POST':
        form = BCMGovernanceForm(request.POST, instance=bcm_governance)
        if form.is_valid():
            form.save()
            messages.success(request, "Governance updated successfully!")
            return redirect('list_bcm_governance')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Governance. Please correct the errors.")
    else:
        form = BCMGovernanceForm(instance=bcm_governance)
    return render(request, 'bcm/bcm_governance.html', {'form': form})



# Delete bcm_governance
def delete_bcm_governance(request, governance_id):
    bcm_governance = get_object_or_404(BCMGovernance, governance_id=governance_id) 
    bcm_governance.delete()
    messages.success(request, "Governance deleted successfully!")
    return redirect('list_bcm_governance')

######
def list_business_impact_analysis(request):
    # Get all records by default
    business_impact_analysiss = BusinessImpactAnalysis.objects.all()
    form = BusinessImpactAnalysisForm()

    
    # Default sorting by bia_id
    sort_by = request.GET.get('sort_by', 'bia_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        business_impact_analysiss = business_impact_analysiss.order_by(sort_by)
    else:
        business_impact_analysiss = business_impact_analysiss.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(business_impact_analysiss, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_business_impact_analysiss = paginator.page(page)
    except PageNotAnInteger:
        paginated_business_impact_analysiss = paginator.page(1)
    except EmptyPage:
        paginated_business_impact_analysiss = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Business Impact Analysis",
        'business_impact_analysiss':business_impact_analysiss, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_business_impact_analysiss': paginated_business_impact_analysiss,
        'rows_per_page': rows_per_page,
        'form': form,
        'reviewed_by_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/business_impact_analysis.html', context)


# Add Oversigh 

def add_business_impact_analysis(request):
    form = BusinessImpactAnalysisForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Business Impact added successfully!")
            return redirect('list_business_impact_analysis')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Business Impact. Please correct the errors.")
    return redirect('list_business_impact_analysis')

# BusinessImpactAnalysis Dashboard
def edit_business_impact_analysis(request, bia_id):
    business_impact_analysis = get_object_or_404(BusinessImpactAnalysis, bia_id=bia_id)
    if request.method == 'POST':
        form = BusinessImpactAnalysisForm(request.POST, instance=business_impact_analysis)
        if form.is_valid():
            form.save()
            messages.success(request, "Business Impact updated successfully!")
            return redirect('list_business_impact_analysis')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Business Impact. Please correct the errors.")
    else:
        form = BusinessImpactAnalysisForm(instance=business_impact_analysis)
    return render(request, 'bcm/business_impact_analysis.html', {'form': form})



# Delete business_impact_analysis
def delete_business_impact_analysis(request, bia_id):
    business_impact_analysis = get_object_or_404(BusinessImpactAnalysis, bia_id=bia_id) 
    business_impact_analysis.delete()
    messages.success(request, "Business Impact deleted successfully!")
    return redirect('list_business_impact_analysis')

######
def list_continuity_risk_assessment(request):
    # Get all records by default
    continuity_risk_assessments = ContinuityRiskAssessment.objects.all()
    form = ContinuityRiskAssessmentForm()

    
    # Default sorting by risk_assessment_id
    sort_by = request.GET.get('sort_by', 'risk_assessment_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        continuity_risk_assessments = continuity_risk_assessments.order_by(sort_by)
    else:
        continuity_risk_assessments = continuity_risk_assessments.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(continuity_risk_assessments, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_continuity_risk_assessments = paginator.page(page)
    except PageNotAnInteger:
        paginated_continuity_risk_assessments = paginator.page(1)
    except EmptyPage:
        paginated_continuity_risk_assessments = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Continuity Risk Assessment",
        'continuity_risk_assessments':continuity_risk_assessments, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_continuity_risk_assessments': paginated_continuity_risk_assessments,
        'rows_per_page': rows_per_page,
        'form': form,
        'review_cycle_choices': ContinuityRiskAssessment._meta.get_field('review_cycle').choices,
        'risk_owner_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/continuity_risk_assessment.html', context)


# Add Oversigh 

def add_continuity_risk_assessment(request):
    form = ContinuityRiskAssessmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Assessment added successfully!")
            return redirect('list_continuity_risk_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Risk Assessment. Please correct the errors.")
    return redirect('list_continuity_risk_assessment')

# ContinuityRiskAssessment Dashboard
def edit_continuity_risk_assessment(request, risk_assessment_id):
    continuity_risk_assessment = get_object_or_404(ContinuityRiskAssessment, risk_assessment_id=risk_assessment_id)
    if request.method == 'POST':
        form = ContinuityRiskAssessmentForm(request.POST, instance=continuity_risk_assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Risk Assessment updated successfully!")
            return redirect('list_continuity_risk_assessment')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Risk Assessment. Please correct the errors.")
    else:
        form = ContinuityRiskAssessmentForm(instance=continuity_risk_assessment)
    return render(request, 'bcm/continuity_risk_assessment.html', {'form': form})



# Delete continuity_risk_assessment
def delete_continuity_risk_assessment(request, risk_assessment_id):
    continuity_risk_assessment = get_object_or_404(ContinuityRiskAssessment, risk_assessment_id=risk_assessment_id) 
    continuity_risk_assessment.delete()
    messages.success(request, "Risk Assessment deleted successfully!")
    return redirect('list_continuity_risk_assessment')

#########
def list_continuity_strategy(request):
    # Get all records by default
    continuity_strategys = ContinuityStrategy.objects.all()
    form = ContinuityStrategyForm()

    
    # Default sorting by strategy_id
    sort_by = request.GET.get('sort_by', 'strategy_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        continuity_strategys = continuity_strategys.order_by(sort_by)
    else:
        continuity_strategys = continuity_strategys.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(continuity_strategys, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_continuity_strategys = paginator.page(page)
    except PageNotAnInteger:
        paginated_continuity_strategys = paginator.page(1)
    except EmptyPage:
        paginated_continuity_strategys = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Continuity Strategy",
        'continuity_strategys':continuity_strategys, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_continuity_strategys': paginated_continuity_strategys,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': ContinuityStrategy._meta.get_field('approval_status').choices,
        'review_frequency_choices': ContinuityStrategy._meta.get_field('review_frequency').choices,
        'reviewer_id_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/continuity_strategy.html', context)


# Add Oversigh 

def add_continuity_strategy(request):
    form = ContinuityStrategyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Strategy added successfully!")
            return redirect('list_continuity_strategy')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Strategy. Please correct the errors.")
    return redirect('list_continuity_strategy')

# ContinuityStrategy Dashboard
def edit_continuity_strategy(request, strategy_id):
    continuity_strategy = get_object_or_404(ContinuityStrategy, strategy_id=strategy_id)
    if request.method == 'POST':
        form = ContinuityStrategyForm(request.POST, instance=continuity_strategy)
        if form.is_valid():
            form.save()
            messages.success(request, "Strategy updated successfully!")
            return redirect('list_continuity_strategy')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Strategy. Please correct the errors.")
    else:
        form = ContinuityStrategyForm(instance=continuity_strategy)
    return render(request, 'bcm/continuity_strategy.html', {'form': form})



# Delete continuity_strategy
def delete_continuity_strategy(request, strategy_id):
    continuity_strategy = get_object_or_404(ContinuityStrategy, strategy_id=strategy_id) 
    continuity_strategy.delete()
    messages.success(request, "Strategy deleted successfully!")
    return redirect('list_continuity_strategy')


######
def list_business_continuity_plan(request):
    # Get all records by default
    business_continuity_plans = BusinessContinuityPlan.objects.all()
    form = BusinessContinuityPlanForm()

    
    # Default sorting by bcp_id
    sort_by = request.GET.get('sort_by', 'bcp_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        business_continuity_plans = business_continuity_plans.order_by(sort_by)
    else:
        business_continuity_plans = business_continuity_plans.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(business_continuity_plans, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_business_continuity_plans = paginator.page(page)
    except PageNotAnInteger:
        paginated_business_continuity_plans = paginator.page(1)
    except EmptyPage:
        paginated_business_continuity_plans = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Business Continuity Plan",
        'business_continuity_plans':business_continuity_plans, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_business_continuity_plans': paginated_business_continuity_plans,
        'rows_per_page': rows_per_page,
        'form': form,
        'approval_status_choices': BusinessContinuityPlan._meta.get_field('approval_status').choices,
        'plan_owner_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/business_continuity_plan.html', context)


# Add Oversigh 

def add_business_continuity_plan(request):
    form = BusinessContinuityPlanForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Continuity Plan added successfully!")
            return redirect('list_business_continuity_plan')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Continuity Plan. Please correct the errors.")
    return redirect('list_business_continuity_plan')

# BusinessContinuityPlan Dashboard
def edit_business_continuity_plan(request, bcp_id):
    business_continuity_plan = get_object_or_404(BusinessContinuityPlan, bcp_id=bcp_id)
    if request.method == 'POST':
        form = BusinessContinuityPlanForm(request.POST, instance=business_continuity_plan)
        if form.is_valid():
            form.save()
            messages.success(request, "Continuity Plan updated successfully!")
            return redirect('list_business_continuity_plan')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Continuity Plan. Please correct the errors.")
    else:
        form = BusinessContinuityPlanForm(instance=business_continuity_plan)
    return render(request, 'bcm/business_continuity_plan.html', {'form': form})



# Delete business_continuity_plan
def delete_business_continuity_plan(request, bcp_id):
    business_continuity_plan = get_object_or_404(BusinessContinuityPlan, bcp_id=bcp_id) 
    business_continuity_plan.delete()
    messages.success(request, "Continuity Plan deleted successfully!")
    return redirect('list_business_continuity_plan')


########
def list_continuity_testing(request):
    # Get all records by default
    continuity_testings = ContinuityTesting.objects.all()
    form = ContinuityTestingForm()

    
    # Default sorting by test_id
    sort_by = request.GET.get('sort_by', 'test_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        continuity_testings = continuity_testings.order_by(sort_by)
    else:
        continuity_testings = continuity_testings.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(continuity_testings, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_continuity_testings = paginator.page(page)
    except PageNotAnInteger:
        paginated_continuity_testings = paginator.page(1)
    except EmptyPage:
        paginated_continuity_testings = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Continuity Testing",
        'continuity_testings':continuity_testings, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_continuity_testings': paginated_continuity_testings,
        'rows_per_page': rows_per_page,
        'form': form,
        'reviewed_by_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/continuity_testing.html', context)


# Add Oversigh 

def add_continuity_testing(request):
    form = ContinuityTestingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Continuity Testing added successfully!")
            return redirect('list_continuity_testing')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Continuity Testing. Please correct the errors.")
    return redirect('list_continuity_testing')

# ContinuityTesting Dashboard
def edit_continuity_testing(request, test_id):
    continuity_testing = get_object_or_404(ContinuityTesting, test_id=test_id)
    if request.method == 'POST':
        form = ContinuityTestingForm(request.POST, instance=continuity_testing)
        if form.is_valid():
            form.save()
            messages.success(request, "Continuity Testing updated successfully!")
            return redirect('list_continuity_testing')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Continuity Testing. Please correct the errors.")
    else:
        form = ContinuityTestingForm(instance=continuity_testing)
    return render(request, 'bcm/continuity_testing.html', {'form': form})



# Delete continuity_testing
def delete_continuity_testing(request, test_id):
    continuity_testing = get_object_or_404(ContinuityTesting, test_id=test_id) 
    continuity_testing.delete()
    messages.success(request, "Continuity Testing deleted successfully!")
    return redirect('list_continuity_testing')

######
def list_incident_activation(request):
    # Get all records by default
    incident_activations = IncidentActivationLog.objects.all()
    form = IncidentActivationLogForm()

    
    # Default sorting by incident_id
    sort_by = request.GET.get('sort_by', 'incident_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        incident_activations = incident_activations.order_by(sort_by)
    else:
        incident_activations = incident_activations.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(incident_activations, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_incident_activations = paginator.page(page)
    except PageNotAnInteger:
        paginated_incident_activations = paginator.page(1)
    except EmptyPage:
        paginated_incident_activations = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Incident Activation",
        'incident_activations':incident_activations, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_incident_activations': paginated_incident_activations,
        'rows_per_page': rows_per_page,
        'form': form,
        'decision_maker_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/incident_activation.html', context)


# Add Oversigh 

def add_incident_activation(request):
    form = IncidentActivationLogForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Incident Activation added successfully!")
            return redirect('list_incident_activation')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Incident Activation. Please correct the errors.")
    return redirect('list_incident_activation')

# IncidentActivationLog Dashboard
def edit_incident_activation(request, incident_id):
    incident_activation = get_object_or_404(IncidentActivationLog, incident_id=incident_id)
    if request.method == 'POST':
        form = IncidentActivationLogForm(request.POST, instance=incident_activation)
        if form.is_valid():
            form.save()
            messages.success(request, "Incident Activation updated successfully!")
            return redirect('list_incident_activation')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Incident Activation. Please correct the errors.")
    else:
        form = IncidentActivationLogForm(instance=incident_activation)
    return render(request, 'bcm/incident_activation.html', {'form': form})



# Delete incident_activation
def delete_incident_activation(request, incident_id):
    incident_activation = get_object_or_404(IncidentActivationLog, incident_id=incident_id) 
    incident_activation.delete()
    messages.success(request, "Incident Activation deleted successfully!")
    return redirect('list_incident_activation')

########
def list_crisis_communication(request):
    # Get all records by default
    crisis_communications = CrisisCommunication.objects.all()
    form = CrisisCommunicationForm()

    
    # Default sorting by communication_id
    sort_by = request.GET.get('sort_by', 'communication_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        crisis_communications = crisis_communications.order_by(sort_by)
    else:
        crisis_communications = crisis_communications.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(crisis_communications, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_crisis_communications = paginator.page(page)
    except PageNotAnInteger:
        paginated_crisis_communications = paginator.page(1)
    except EmptyPage:
        paginated_crisis_communications = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "Crisis Communication",
        'crisis_communications':crisis_communications, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_crisis_communications': paginated_crisis_communications,
        'rows_per_page': rows_per_page,
        'form': form,
        'acknowledgment_status_choices': CrisisCommunication._meta.get_field('acknowledgment_status').choices,
        'sent_by_choices': Staff.objects.all(),
        'incident_id_choices': IncidentActivationLog.objects.all(),
    }
    return render(request, 'bcm/crisis_communication.html', context)


# Add Oversigh 

def add_crisis_communication(request):
    form = CrisisCommunicationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Crisis Communication added successfully!")
            return redirect('list_crisis_communication')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Crisis Communication. Please correct the errors.")
    return redirect('list_crisis_communication')

# CrisisCommunication Dashboard
def edit_crisis_communication(request, communication_id):
    crisis_communication = get_object_or_404(CrisisCommunication, communication_id=communication_id)
    if request.method == 'POST':
        form = CrisisCommunicationForm(request.POST, instance=crisis_communication)
        if form.is_valid():
            form.save()
            messages.success(request, "Crisis Communication updated successfully!")
            return redirect('list_crisis_communication')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Crisis Communication. Please correct the errors.")
    else:
        form = CrisisCommunicationForm(instance=crisis_communication)
    return render(request, 'bcm/crisis_communication.html', {'form': form})



# Delete crisis_communication
def delete_crisis_communication(request, communication_id):
    crisis_communication = get_object_or_404(CrisisCommunication, communication_id=communication_id) 
    crisis_communication.delete()
    messages.success(request, "Crisis Communication deleted successfully!")
    return redirect('list_crisis_communication')

######
def list_bcm_program_review(request):
    # Get all records by default
    bcm_program_reviews = BCMProgramReview.objects.all()
    form = BCMProgramReviewForm()

    
    # Default sorting by review_id
    sort_by = request.GET.get('sort_by', 'review_id')
    order = request.GET.get('order', 'asc')

    # Toggle order on each click
    if order == 'asc':
        bcm_program_reviews = bcm_program_reviews.order_by(sort_by)
    else:
        bcm_program_reviews = bcm_program_reviews.order_by(F(sort_by).desc())

    # Pagination setup
    rows_per_page = request.GET.get('rows_per_page', 10)
    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = 10

    paginator = Paginator(bcm_program_reviews, rows_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_bcm_program_reviews = paginator.page(page)
    except PageNotAnInteger:
        paginated_bcm_program_reviews = paginator.page(1)
    except EmptyPage:
        paginated_bcm_program_reviews = paginator.page(paginator.num_pages)

    
    # Pass necessary context to the template
    context = {
        'page_title': "BCM Program Review",
        'bcm_program_reviews':bcm_program_reviews, 
        'current_sort': sort_by,
        'current_order': order,       
        'paginated_bcm_program_reviews': paginated_bcm_program_reviews,
        'rows_per_page': rows_per_page,
        'form': form,
        'compliance_status_choices': BCMProgramReview._meta.get_field('compliance_status').choices,
        'reviewer_id_choices': Staff.objects.all(),
    }
    return render(request, 'bcm/bcm_program_review.html', context)


# Add Oversigh 

def add_bcm_program_review(request):
    form = BCMProgramReviewForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Review added successfully!")
            return redirect('list_bcm_program_review')
        else:
            print(form.errors)
            messages.error(request, "Failed to add Review. Please correct the errors.")
    return redirect('list_bcm_program_review')

# BCMProgramReview Dashboard
def edit_bcm_program_review(request, review_id):
    bcm_program_review = get_object_or_404(BCMProgramReview, review_id=review_id)
    if request.method == 'POST':
        form = BCMProgramReviewForm(request.POST, instance=bcm_program_review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully!")
            return redirect('list_bcm_program_review')
        else:
            print(form.errors)
            messages.error(request, "Failed to update Review. Please correct the errors.")
    else:
        form = BCMProgramReviewForm(instance=bcm_program_review)
    return render(request, 'bcm/bcm_program_review.html', {'form': form})



# Delete bcm_program_review
def delete_bcm_program_review(request, review_id):
    bcm_program_review = get_object_or_404(BCMProgramReview, review_id=review_id) 
    bcm_program_review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('list_bcm_program_review')
