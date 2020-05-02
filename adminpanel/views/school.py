import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from ankadescankaya.views import current_user_group
from exam.models import School, Department


def admin_all_schools(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    schools = School.objects.all()
    departments = Department.objects.all()
    context = {
        "userGroup": userGroup,
        "schools": schools,
        "departments": departments,
    }
    return render(request, "adminpanel/exam/all-schools.html", context)


def admin_add_school(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
    }
    if request.method == "POST":
        instance = School()
        title = request.POST.get("title")
        instance.title = title
        instance.isActive = True
        instance.creator = request.user
        instance.createdDate = datetime.datetime.now()
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Okul başarıyla eklendi.")
        return redirect("admin_add_school")
    return render(request, "adminpanel/exam/add/add-school.html", context)
