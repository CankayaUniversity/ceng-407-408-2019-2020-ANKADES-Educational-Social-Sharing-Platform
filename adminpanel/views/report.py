import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ankadescankaya.views import current_user_group
from support.models import Support, ReportSubject
from support.models import Report


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
    return render(request, "adminpanel/support/active-reports.html", context)


@login_required(login_url="login_admin")
def admin_add_report_subject(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == "admin" or userGroup == "moderator":
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            isActive = request.POST.get("isActive") == "on"
            isRoot = request.POST.get("isRoot") == "on"
            isCategory = request.POST.get("isCategory") == "on"
            new_report_subject = ReportSubject(title=title, description=description, isActive=isActive, isRoot=isRoot,
                                               isCategory=isCategory)
            new_report_subject.createdDate = datetime.datetime.now()
            new_report_subject.creator = request.user
            new_report_subject.save()
            new_report_subject.parentId = new_report_subject
            new_report_subject.save()
            messages.success(request, "Şikayet başlığı başarıyla oluşturuldu.")
        return render(request, "adminpanel/support/add-report-subject.html", {"userGroup": userGroup})
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_all_report_subjects(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    reports = ReportSubject.objects.all()
    context = {
        "userGroup": userGroup,
        "reports": reports,
    }
    return render(request, "adminpanel/support/all-report-subjects.html", context)


@login_required(login_url="login_admin")
def admin_all_reports(request):
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
