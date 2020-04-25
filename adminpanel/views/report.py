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
    if userGroup == "admin":
        reports = Report.objects.all()
        context = {
            "userGroup": userGroup,
            "reports": reports,
        }
        return render(request, "adminpanel/support/all-reports.html", context)
    else:
        return messages.error(request, "Yetkiniz yok")
        return redirect("admin_dashboard")
