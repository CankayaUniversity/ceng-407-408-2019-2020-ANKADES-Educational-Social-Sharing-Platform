import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import AccountLogs
from account.views.views import current_user_group
from adminpanel.models import AdminLogs


@login_required(login_url="login_admin")
def admin_all_logs(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    adminLogs = AdminLogs.objects.all().order_by('-createdDate')
    accountLogs = AccountLogs.objects.all().order_by('-createdDate')
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "adminLogs": adminLogs,
        "accountLogs": accountLogs,
    }
    return render(request, "adminpanel/log/all-logs.html", context)


@login_required(login_url="login_admin")
def admin_admin_logs(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    adminLogs = AdminLogs.objects.all().order_by('-createdDate')
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "adminLogs": adminLogs,
    }
    return render(request, "adminpanel/log/admin-logs.html", context)


@login_required(login_url="login_admin")
def admin_account_logs(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    accountLogs = AccountLogs.objects.all().order_by('-createdDate')
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "accountLogs": accountLogs,
    }
    return render(request, "adminpanel/log/account-logs.html", context)