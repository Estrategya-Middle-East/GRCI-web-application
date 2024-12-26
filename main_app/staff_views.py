import os
import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.forms import modelformset_factory
from django.forms import inlineformset_factory

#Excel library
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

import pandas as pd

from .forms import *
from .models import *


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_users = User.objects.filter(department=staff.department).count()

    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.first_name) ,#+ ' (' + str(staff.department) + ')',
        'total_users': total_users,

    }
    return render(request, 'staff_template/home_content.html', context)

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
            survey = form.cleaned_data.get('survey')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.user.servey = survey
                user.user.department = department
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('manage_user_staff'))
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
                return redirect(reverse('manage_department_staff'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_department_template.html', context)

def manage_user(request):
    users = CustomUser.objects.filter(user_type=3)
    context = {
        'users': users,
        'page_title': 'Manage Users'
    }
    return render(request, "staff_template/staff_manage_user.html", context)

def manage_department(request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
        'page_title': 'Manage Departments'
    }
    return render(request, "staff_template/staff_manage_department.html", context)



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
                return redirect(reverse('staff_edit_user', args=[user_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    return render(request, "hod_template/edit_user_template.html", context)

def edit_department(request, department_id):
    instance = get_object_or_404(Department, id=department_id)
    form = DepartmentForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'department_id': department_id,
        'page_title': 'Edit Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                department = Department.objects.get(id=department_id)
                department.name = name
                department.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_department_template.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, user__id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect(reverse('manage_user_staff'))


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    try:
        department.delete()
        messages.success(request, "Department deleted successfully!")
    except Exception:
        messages.error(
            request, "Sorry, some users are assigned to this department already. Kindly change the affected user department and try again")
    return redirect(reverse('manage_department_staff'))

@csrf_exempt
def get_users(request):
    session_id = request.POST.get('session')
    try:
        session = get_object_or_404(Session, id=session_id)
        users = User.objects.filter(
            session=session)
        user_data = []
        for user in users:
            data = {
                    "id": user.id,
                    "name": user.admin.last_name + " " + user.admin.first_name
                    }
            user_data.append(data)
        return JsonResponse(json.dumps(user_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None,instance=staff)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = staff.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                staff.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "staff_template/staff_view_profile.html", context)

    return render(request, "staff_template/staff_view_profile.html", context)


@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def staff_view_notification(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "staff_template/staff_view_notification.html", context)

