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
        "icon": "nav-icon fas fa-shield-alt",
        "url": "/erm/",
        "action_text": "Access and Manage Enterprise Risks Now",
        "code": "SUBSCRIBE2024",
        "visible": True,
    },
    {
        "id": 2,
        "name": "IAM",
        "description": "Internal Audit Management",
        "icon": "nav-icon fas fa-search-dollar",
        "url": "/iam/",
        "action_text": "Initiate and Oversee Your Audits Today",
        "code": "SUBSCRIBE2024",
        "visible": False,
    },
    {
        "id": 3,
        "name": "BCM",
        "description": "Business Continuity Management",
        "icon": "nav-icon fas fa-business-time",
        "url": "/bcm/",
        "action_text": "Plan and Safeguard Business Continuity Measures",
        "code": "SUBSCRIBE2024",
        "visible": False,
    },
    {
        "id": 4,
        "name": "GM",
        "description": "Governance Management",
        "icon": "nav-icon fas fa-gavel",
        "url": "/gm/",
        "action_text": "Strengthen and Implement Governance Best Practices",
        "code": "SUBSCRIBE2024",
        "visible": False,
    },
    {
        "id": 5,
        "name": "ISM",
        "description": "InfoSec Management",
        "icon": "nav-icon fas fa-lock",
        "url": "/ism/",
        "action_text": "Secure and Enhance Information Security Controls",
        "code": "SUBSCRIBE2024",
        "visible": False,
    },
    {
        "id": 6,
        "name": "CM",
        "description": "Compliance Management",
        "icon": "nav-icon fas fa-check-circle",
        "url": "/cm/",
        "action_text": "Verify and Maintain Compliance Standards Easily",
        "code": "SUBSCRIBE2024",
        "visible": False,
    },
    {
        "id": 7,
        "name": "BPM",
        "description": "Business Process Management",
        "icon": "nav-icon fas fa-cogs",
        "url": "/bpm/",
        "action_text": "Streamline and Improve Business Processes",
        "code": "SUBSCRIBE2024",
        "visible": False,
    },
    {
        "id": 8,
        "name": "PioNeer+",
        "description": "AI Engine (PioNeer+)",
        "icon": "nav-icon fas fa-brain",
        "url": "/pioneer/",
        "action_text": "Leverage Advanced AI for Smarter Solutions",
        "code": "SUBSCRIBE2024",
        "visible": True,
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
            try:
                # Update the department instance
                department = Department.objects.get(id=department_id)
                department.name = name
                department.description = description  
                department.save()
                messages.success(request, "Successfully Updated")
            except Exception as e:
                messages.error(request, f"Could Not Update: {e}")
        else:
            messages.error(request, "Could Not Update: Invalid Data")

    return render(request, 'hod_template/edit_department_template.html', context)

def add_session(request):
    form = SessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "hod_template/add_session_template.html", context)


def manage_session(request):
    sessions = Session.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "hod_template/manage_session.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(Session, id=session_id)
    form = SessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_session_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_session_template.html", context)

    else:
        return render(request, "hod_template/edit_session_template.html", context)


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


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    try:
        session.delete()
        messages.success(request, "Session deleted successfully!")
    except Exception:
        messages.error(
            request, "There are users assigned to this session. Please move them to another session.")
    return redirect(reverse('manage_session'))

