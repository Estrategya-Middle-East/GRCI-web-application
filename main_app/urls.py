"""college_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from . import hod_views, staff_views, user_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/nav/", hod_views.admin_nav, name='admin_nav'),
    path('app_store/', hod_views.app_store, name='app_store'),
    path("submit_subscription/", hod_views.submit_subscription, name="submit_subscription"),
    path('toggle_visibility/<int:module_id>/', hod_views.toggle_visibility, name='toggle_visibility'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("department/add", hod_views.add_department, name='add_department'),
    path('add-group/', hod_views.add_group, name='add_group'),
    path('group_list/', hod_views.group_list, name='group_list'),
    
    # staff
    path("staff/department/add", staff_views.add_department, name='add_department_staff'),

    path("send_user_notification/", hod_views.send_user_notification,
         name='send_user_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("view/notification/", hod_views.admin_view_notification,
         name="admin_view_notification"),
    
    path("admin_notify_user", hod_views.admin_notify_user,
         name='admin_notify_user'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    

    path("user/add/", hod_views.add_user, name='add_user'),
    # staff
    path("staff/user/add/", staff_views.add_user, name='add_user_staff'),


    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("user/manage/", hod_views.manage_user, name='manage_user'),
    # staff
    path("staff/user/manage/", staff_views.manage_user, name='manage_user_staff'),

    path("department/manage/", hod_views.manage_department, name='manage_department'),
    # staff
    path("staff/department/manage", staff_views.manage_department, name='manage_department_staff'),

    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),
    path("staff/edit/<int:staff_id>",
         hod_views.edit_staff, name='edit_staff'),

    path("department/delete/<int:department_id>",
         hod_views.delete_department, name='delete_department'),
    # staff
    path("staff/department/delete/<int:department_id>",
         staff_views.delete_department, name='staff_delete_department'),


    

    path("user/delete/<int:user_id>",
         hod_views.delete_user, name='delete_user'),
    # staff
    path("staff/user/delete/<int:user_id>",
         staff_views.delete_user, name='staff_delete_user'),

    path("user/edit/<int:user_id>",
         hod_views.edit_user, name='edit_user'),
    # staff
    path("staff/user/edit/<int:user_id>", staff_views.edit_user, name='staff_edit_user'),

    path("department/edit/<int:department_id>",
         hod_views.edit_department, name='edit_department'),
    # staff
    path("staff/department/edit/<int:department_id>", staff_views.edit_department, name='staff_edit_department'),


    # Staff
path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),

    path("staff/get_users/", staff_views.get_users, name='get_users'),

    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),



    # User
    path("user/home/", user_views.user_home, name='user_home'),
    path("user/view/profile/", user_views.user_view_profile,
         name='user_view_profile'),
    path("user/fcmtoken/", user_views.user_fcmtoken,
         name='user_fcmtoken'),
    path("user/view/notification/", user_views.user_view_notification,
         name="user_view_notification"),

]