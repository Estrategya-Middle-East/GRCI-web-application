import os
import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.template.loader import render_to_string
#Excel library for the download function
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

import pandas as pd

from .forms import *
from .models import *
from django.contrib.auth.models import Group
from .forms import GroupForm

def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('group_list')  # Redirect to a page that lists groups
    else:
        form = GroupForm()

    # Group permissions by model
    permissions_by_model = {}
    for perm in Permission.objects.all():
        model_name = f"{perm.content_type.app_label} | {perm.content_type.model}"
        if model_name not in permissions_by_model:
            permissions_by_model[model_name] = []
        permissions_by_model[model_name].append(perm)

    # Pad permissions to ensure 4 columns
    for model_name, perms in permissions_by_model.items():
        padding_needed = (4 - len(perms) % 4) % 4
        permissions_by_model[model_name].extend([None] * padding_needed)

    return render(request, 'hod_template/add_group.html', {
        'form': form,
        'permissions_by_model': permissions_by_model,
        'page_title': "Add Role",
    })

def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            group.permissions.set(request.POST.getlist('permissions'))
            return redirect('group_list')  # Redirect to a page that lists groups
    else:
        form = GroupForm(instance=group)

    # Group permissions by model
    permissions_by_model = {}
    for perm in Permission.objects.all():
        model_name = f"{perm.content_type.app_label} | {perm.content_type.model}"
        if model_name not in permissions_by_model:
            permissions_by_model[model_name] = []
        permissions_by_model[model_name].append(perm)

    # Pad permissions to ensure 4 columns
    for model_name, perms in permissions_by_model.items():
        padding_needed = (4 - len(perms) % 4) % 4
        permissions_by_model[model_name].extend([None] * padding_needed)

    # Pass current permissions of the group for pre-checking
    current_permissions = group.permissions.all()

    return render(request, 'hod_template/edit_group.html', {
        'form': form,
        'permissions_by_model': permissions_by_model,
        'current_permissions': current_permissions,
        'page_title': "Edit Role",
    })


def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('group_list')


def group_list(request):
    groups = Group.objects.all()
    return render(request, 'hod_template/group_list.html', 
    {'groups': groups,'page_title': "Roles",})


def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_users = User.objects.all().count()
    total_department = Department.objects.all().count()

    # Total Surveys and users in Each Department
    department_all = Department.objects.all()
    department_name_list = []
    user_count_list_in_department = []

    for department in department_all:
        users = User.objects.filter(department_id=department.id).count()
        department_name_list.append(department.name)
        user_count_list_in_department.append(users)

    # For Users

    user_name_list=[]

    users = User.objects.all()
    for user in users:
        user_name_list.append(user.admin.first_name)

    context = {
        'page_title': "Dashboard",
        'total_users': total_users,
        'total_staff': total_staff,
        'total_department': total_department,
        "user_name_list": user_name_list,
        "user_count_list_in_department": user_count_list_in_department,
        "department_name_list": department_name_list,

    }
    return render(request, 'hod_template/home_content.html', context)

# Define modules and their default visibility
MODULES = [
    {
        "id": 1,
        "name": "ERM",
        "description": "Enterprise Risk Management",
        "about":"Start Managing Risks Today.",
        "icon": "nav-icon fas fa-shield-alt",
        "url": "/erm/risk_intelligence/",
        "action_text": "Access and Manage Enterprise Risks Now",
        "code": "SUBSCRIBE2024",
        "visible": True,
        "info": "Proactively identify, assess, and mitigate risks to safeguard your enterprise.",
    },
    {
        "id": 2,
        "name": "IAM",
        "description": "Internal Audit Management",
        "about":"Audit with Confidence Now.",
        "icon": "nav-icon fas fa-search-dollar",
        "url": "/iam/",
        "action_text": "Initiate and Oversee Your Audits Today",
        "code": "SUBSCRIBE2024",
        "visible": False,
        "info": "Streamline your audit processes and ensure transparency in governance.",
    },
    {
        "id": 3,
        "name": "BCM",
        "description": "Business Continuity Management",
        "about":" Build Resilience Today.",
        "icon": "nav-icon fas fa-business-time",
        "url": "/bcm/",
        "action_text": "Plan and Safeguard Business Continuity Measures",
        "code": "SUBSCRIBE2024",
        "visible": False,
        "info": "Prepare your organization for disruptions with robust continuity planning.",
    },
    {
        "id": 4,
        "name": "GM",
        "description": "Governance Management",
        "about":"Optimize Governance Frameworks Now.",
        "icon": "nav-icon fas fa-gavel",
        "url": "/gm/",
        "action_text": "Strengthen and Implement Governance Best Practices",
        "code": "SUBSCRIBE2024",
        "visible": False,
        "info": "Ensure effective governance and align your organization with regulatory standards.",
    },
    {
        "id": 5,
        "name": "ISM",
        "description": "InfoSec Management",
        "about":" Enhance Information Security Today.",
        "icon": "nav-icon fas fa-lock",
        "url": "/ism/",
        "action_text": "Secure and Enhance Information Security Controls",
        "code": "SUBSCRIBE2024",
        "visible": False,
        "info": "Secure your critical information and protect your organization from threats.",
    },
    {
        "id": 6,
        "name": "CM",
        "description": "Compliance Management",
        "about":"Stay Compliant Effortlessly.",
        "icon": "nav-icon fas fa-check-circle",
        "url": "/cm/",
        "action_text": "Verify and Maintain Compliance Standards Easily",
        "code": "SUBSCRIBE2024",
        "visible": False,
        "info": "Simplify compliance processes and stay ahead of regulatory requirements.",
    },
    {
        "id": 7,
        "name": "BPM",
        "description": "Business Process Management",
        "about":"Optimize Your Processes Now.",
        "icon": "nav-icon fas fa-cog",
        "url": "/bpm/",
        "action_text": "Streamline and Improve Business Processes",
        "code": "SUBSCRIBE2024",
        "visible": False,
        "info": "Streamline workflows and improve operational efficiency across your business.",
    },
    {
        "id": 8,
        "name": "PioNeer+",
        "description": "AI Engine (PioNeer+)",
        "about":"Unlock Predictive Power with GenAI.",
        "icon": "nav-icon fas fa-brain",
        "url": "/pioneer/chat/",
        "action_text": "Leverage Advanced AI for Smarter Solutions",
        "code": "SUBSCRIBE2024",
        "visible": True,
        "info": "Leverage advanced AI-driven insights to predict risks and drive smarter decisions.",
    },
    {
        "id": 9,
        "name": "About GRCi",
        # "description": "AI Engine (PioNeer+)",
        "about":"Discover how GRCi can transform your business today.",
        "icon": "nav-icon fas fa-info",
        "url": "#",
        "action_text": "Leverage Advanced AI for Smarter Solutions",
        "code": "SUBSCRIBE2024",
        "visible": True,
        "info": "GRCi is your trusted platform for streamlining GRC processes across your organization.",
    },
]

def submit_subscription(request):
    if request.method == "POST":
        module_id = int(request.POST.get("module_id"))
        subscription_code = request.POST.get("subscription_code")

        # Find the module by ID
        module = next((m for m in MODULES if m["id"] == module_id), None)

        if module:
            valid_code = module["code"]  # Get the valid code from the module
            if subscription_code == valid_code:
                module["visible"] = True  # Update visibility
                return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "Invalid subscription code."})

    return JsonResponse({"success": False, "error": "Invalid request method."})

def admin_nav(request):
    # Filter visible modules
    visible_modules = [module for module in MODULES if module["visible"]]
    context = {
        'page_title': "Navigation",
        'grouped_modules': [visible_modules[i:i + 3] for i in range(0, len(visible_modules), 3)],
        'visible_modules': visible_modules,  # Pass visible modules for the sidebar
    }
    return render(request, 'hod_template/navigation.html', context)

def app_store(request):
    context = {
        'page_title': "Apps",
        'grouped_modules': [MODULES[i:i + 3] for i in range(0, len(MODULES), 3)],
        'visible_modules': [module for module in MODULES if module["visible"]],
    }
    return render(request, 'app_store.html', context)

@csrf_exempt
def toggle_visibility(request, module_id):
    if request.method == "POST":
        # Find and toggle the visibility of the module
        for module in MODULES:
            if module["id"] == module_id:
                module["visible"] = not module["visible"]
                break
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            department = form.cleaned_data.get('department')
            role = form.cleaned_data.get('role')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.department = department
                user.staff.role = role
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_staff_template.html', context)


def add_user(request):
    form = UserForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add User'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            department = form.cleaned_data.get('department')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.user.department = department
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_user'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_user_template.html', context)


def add_department(request):
    form = DepartmentForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                department = Department()
                department.name = name
                department.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_department'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_department_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Staff'
    }
    return render(request, "hod_template/manage_staff.html", context)


def manage_user(request):
    users = CustomUser.objects.filter(user_type=3)
    context = {
        'users': users,
        'page_title': 'Manage Users'
    }
    return render(request, "hod_template/manage_user.html", context)


def manage_department(request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
        'page_title': 'Manage Departments'
    }
    return render(request, "hod_template/manage_department.html", context)

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Staff'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            department = form.cleaned_data.get('department')
            role = form.cleaned_data.get('role')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                staff.department = department
                staff.role = role
                user.save()
                staff.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=staff_id)
        staff = Staff.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)


def edit_user(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    form = UserForm(request.POST or None, instance=user_profile)
    context = {
        'form': form,
        'user_id': user_id,
        'page_title': 'Edit User'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            department = form.cleaned_data.get('department')
            survey = form.cleaned_data.get('survey')
            passport = request.FILES.get('profile_pic') or None
            try:
                # Update CustomUser
                user = user_profile.admin
                if passport is not None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                user.save()

                # Update User fields
                user_profile.department = department
                user_profile.survey = survey
                user_profile.save()

                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_user', args=[user_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    return render(request, "hod_template/edit_user_template.html", context)



def edit_department(request, department_id):
    instance = get_object_or_404(Department, id=department_id)  # Retrieve the department instance
    form = DepartmentForm(request.POST or None, instance=instance)  # Bind the form to the instance
    context = {
        'form': form,
        'department_id': department_id,
        'page_title': 'Edit Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            # Retrieve the cleaned data for name and description
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            org_chart_level = form.cleaned_data.get('org_chart_level')
            parent = form.cleaned_data.get('parent')
            introduction_section = form.cleaned_data.get('introduction_section')
            primary_responsibilities_section = form.cleaned_data.get(' primary_responsibilities_section')
            team_section = form.cleaned_data.get('team_section')
            governance_section  = form.cleaned_data.get('governance_section')
            policies_section = form.cleaned_data.get('policies_section')
            challenges_section = form.cleaned_data.get('challenges_section')
            performance_section = form.cleaned_data.get('performance_section')
            technology_section = form.cleaned_data.get('technology_section')
            interaction_section = form.cleaned_data.get('interaction_section')
            regulations_section = form.cleaned_data.get('regulations_section')
            plans_section = form.cleaned_data.get('plans_section')
            raci_matrix_section = form.cleaned_data.get('raci_matrix_section')
            authority_delegation_section = form.cleaned_data.get('authority_delegation_section')
            mis_section = form.cleaned_data.get('mis_section')
            departmental_swot_section = form.cleaned_data.get('departmental_swot_section')
            annual_budget_section = form.cleaned_data.get('annual_budget_section')
            other_information_section = form.cleaned_data.get('other_information_section')
            try:
                # Update the department instance
                department = Department.objects.get(id=department_id)
                department.name = name
                department.description = description  
                department.org_chart_level = org_chart_level  
                department.parent = parent  
                department.introduction_section = introduction_section
                department.primary_responsibilities_section =  primary_responsibilities_section
                department.team_section = team_section
                department.governance_section  = governance_section
                department.policies_section = policies_section
                department.challenges_section = challenges_section
                department.performance_section = performance_section
                department.technology_section = technology_section
                department.interaction_section = interaction_section
                department.regulations_section = regulations_section
                department.plans_section = plans_section
                department.raci_matrix_section = raci_matrix_section
                department.authority_delegation_section = authority_delegation_section
                department.mis_section = mis_section
                department.departmental_swot_section = departmental_swot_section
                department.annual_budget_section = annual_budget_section
                department.other_information_section =  other_information_section
                department.save()
                messages.success(request, "Successfully Updated")
            except Exception as e:
                messages.error(request, f"Could Not Update: {e}")
        else:
            messages.error(request, "Could Not Update: Invalid Data")

    return render(request, 'hod_template/edit_department_template.html', context)

def org_dashboard(request):
    
    
    # Organizational structure tree logic

    def build_department_tree(parent_department=None):
        # Query departments with the specified parent
        departments = Department.objects.filter(parent=parent_department)

        # Build tree data recursively
        department_data = []
        for department in departments:
            # Calculate the total staff, including children
            child_departments = build_department_tree(department)
            total_staff = department.staff.count() + sum(child["total_staff"] for child in child_departments)

            # Build the current department's data
            department_data.append({
                "name": department.name,
                "id": department.id,
                "url": reverse('edit_department', args=[department.id]),
                "staff_count": department.staff.count(),
                "total_staff": total_staff,
                "children": child_departments,
                "tooltip": {
                    "formatter": f"Total Staff: {total_staff}"  # Only show total staff
                },
            })
        return department_data

    # Create the org chart data starting from top-level departments (those without a parent)
    org_chart_data = {
        "name": "CEO",
        "id": None,
        "url": "",
        "staff_count": 0,
        "total_staff": sum(
            department.staff.count() +
            sum(child["total_staff"] for child in build_department_tree(department))
            for department in Department.objects.filter(parent=None)
        ),
        "children": build_department_tree(),
        "tooltip": {
            "formatter": f"Total Staff: {sum(department.staff.count() + sum(child['total_staff'] for child in build_department_tree(department)) for department in Department.objects.filter(parent=None))}"
        }
    }

    # Pass to the template
    context = {
        'page_title': "Organizational Structure",
        'org_chart_data': json.dumps(org_chart_data),  # Ensure data is JSON-serializable
    }

    return render(request, 'hod_template/org_dashboard.html', context)

@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


def admin_notify_user(request):
    user = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Users",
        'users': user
    }
    return render(request, "hod_template/user_notification.html", context)

def admin_view_notification(request):
    admin = get_object_or_404(Admin, admin=request.user)
    notifications = Notificationadmin.objects.filter(admin=admin)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "hod_template/admin_view_notification.html", context)


@csrf_exempt
def send_user_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    user = get_object_or_404(User, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "User Management System",
                'body': message,
                'click_action': reverse('user_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': user.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationUser(user=user, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "User Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, staff__id=staff_id)
    staff.delete()
    messages.success(request, "Staff deleted successfully!")
    return redirect(reverse('manage_staff'))


def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, user__id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect(reverse('manage_user'))


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    try:
        department.delete()
        messages.success(request, "Department deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some users are assigned to this department already. Kindly change the affected user department and try again")
    return redirect(reverse('manage_department'))


