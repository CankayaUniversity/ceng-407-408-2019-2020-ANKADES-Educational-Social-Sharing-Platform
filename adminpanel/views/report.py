from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ankadescankaya.views import current_user_group
from support.models import Report


@login_required(login_url="login_admin")
def admin_reports(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    reports = Report.objects.all()
    context = {
        "userGroup": userGroup,
        "reports": reports,
    }
    return render(request, "adminpanel/support/all-reports.html", context)


@login_required(login_url="login_admin")
def admin_active_reports(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    activeReports = Report.objects.filter(isActive=True)
    context = {
        "userGroup": userGroup,
        "activeReports": activeReports,
    }
    return render(request, "adminpanel/support/all-reports.html", context)
