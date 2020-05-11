from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.models import AccountLogs
from adminpanel.models import AdminLogs
from ankadescankaya.views.views import current_user_group


@login_required(login_url="login_admin")
def admin_all_logs(request):
    userGroup = current_user_group(request, request.user)
    adminLogs = AdminLogs.objects.all().order_by('-createdDate')
    accountLogs = AccountLogs.objects.all().order_by('-createdDate')
    context = {
        "userGroup": userGroup,
        "adminLogs": adminLogs,
        "accountLogs": accountLogs,
    }
    return render(request, "adminpanel/log/all-logs.html", context)


@login_required(login_url="login_admin")
def admin_admin_logs(request):
    """
    :rtype: object
    """
    userGroup = current_user_group(request, request.user)
    adminLogs = AdminLogs.objects.all().order_by('-createdDate')
    context = {
        "userGroup": userGroup,
        "adminLogs": adminLogs,
    }
    return render(request, "adminpanel/log/admin-logs.html", context)


@login_required(login_url="login_admin")
def admin_account_logs(request):
    userGroup = current_user_group(request, request.user)
    accountLogs = AccountLogs.objects.all().order_by('-createdDate')
    context = {
        "userGroup": userGroup,
        "accountLogs": accountLogs,
    }
    return render(request, "adminpanel/log/account-logs.html", context)