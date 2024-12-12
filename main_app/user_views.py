import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.db.models import Count
from django.db.models import Max

from .forms import *
from .models import *


def user_home(request):
    user = get_object_or_404(User, admin=request.user)
    """total_survey = Survey.objects.filter(department=user.department).count()
    total_attendance = AttendanceReport.objects.filter(user=user).count()
    total_present = AttendanceReport.objects.filter(user=user, status=True).count()
    if total_attendance == 0:  # Don't divide. DivisionByZero
        percent_absent = percent_present = 0
    else:
        percent_present = math.floor((total_present/total_attendance) * 100)
        percent_absent = math.ceil(100 - percent_present)
    survey_name = []
    data_present = []
    data_absent = []
    surveys = Survey.objects.filter(department=user.department)
    for survey in surveys:
        attendance = Attendance.objects.filter(survey=survey)
        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=True, user=user).count()
        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance, status=False, user=user).count()
        survey_name.append(survey.name)
        data_present.append(present_count)
        data_absent.append(absent_count)"""
    context = {
        
        'page_title': 'Home',

    }
    """ 'page_title': 'User Homepage - ' + str(user.admin.first_name) ,
        'total_attendance': total_attendance,
        'percent_present': percent_present,
        'percent_absent': percent_absent,
        'total_survey': total_survey,
        'surveys': surveys,
        'data_present': data_present,
        'data_absent': data_absent,
        'data_name': survey_name,"""
    return render(request, 'user_template/home_content.html', context)

"""
@ csrf_exempt
def user_view_attendance(request):
    user = get_object_or_404(User, admin=request.user)
    if request.method != 'POST':
        department = get_object_or_404(Department, id=user.department.id)
        context = {
            #'surveys': Survey.objects.filter(department=department),
            'page_title': 'View Attendance'
        }
        return render(request, 'user_template/user_view_attendance.html', context)
    else:
        survey_id = request.POST.get('survey')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            survey = get_object_or_404(Survey, id=survey_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), survey=survey)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, user=user)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None


def user_apply_leave(request):
    form = LeaveReportUserForm(request.POST or None)
    user = get_object_or_404(User, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportUser.objects.filter(user=user),
        'page_title': 'Apply for leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.user = user
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('user_apply_leave'))
            except Exception:
                messages.error(request, "Could not submit")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "user_template/user_apply_leave.html", context)


def user_feedback(request):
    form = FeedbackUserForm(request.POST or None)
    user = get_object_or_404(User, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackUser.objects.filter(user=user),
        'page_title': 'User Feedback'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.user = user
                obj.save()
                messages.success(
                    request, "Feedback submitted for review")
                return redirect(reverse('user_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "user_template/user_feedback.html", context)
"""

def user_view_profile(request):
    user = get_object_or_404(User, admin=request.user)
    form = UserEditForm(request.POST or None, request.FILES or None,
                           instance=user)
    context = {'form': form,
               'page_title': 'Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = user.admin
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
                user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('user_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "user_template/user_view_profile.html", context)


@csrf_exempt
def user_fcmtoken(request):
    token = request.POST.get('token')
    user_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        user_user.fcm_token = token
        user_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def user_view_notification(request):
    user = get_object_or_404(User, admin=request.user)
    notifications = NotificationUser.objects.filter(user=user)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "user_template/user_view_notification.html", context)



