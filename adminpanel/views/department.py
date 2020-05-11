import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from ankadescankaya.views.views import current_user_group
from exam.models import School, Department


def admin_all_departments(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = School.objects.get(slug=slug)
    except:
        messages.error(request, "Böyle bir okul bulunamadı.")
        return redirect("admin_all_schools")
    userGroup = current_user_group(request, request.user)
    departments = Department.objects.filter(schoolId=instance)
    context = {
        "userGroup": userGroup,
        "departments": departments,
    }
    return render(request, "adminpanel/exam/all-departments.html", context)


def admin_add_department(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == "moderator" or userGroup == "admin" or userGroup == "ogretmen":
        schools = School.objects.all().order_by('slug')
        context = {
            "userGroup": userGroup,
            "schools": schools,
        }
        if request.method == "POST":
            instance = Department()
            schoolId = request.POST["schoolId"]
            title = request.POST.get("title")
            check = Department.objects.filter(schoolId_id=schoolId, title=title)
            if check:
                messages.error(request, "Bu okula daha önce " + str(title) + " bölümü tanımlanmış.")
                return redirect("admin_add_department")
            else:
                instance.title = title
                instance.isActive = True
                instance.creator = request.user
                instance.createdDate = datetime.datetime.now()
                instance.updatedDate = datetime.datetime.now()
                instance.schoolId_id = schoolId
                instance.departmentCode = get_random_string(length=32)
                instance.save()
                messages.success(request, "Bölüm başarıyla eklendi.")
                return redirect("admin_add_department")
        return render(request, "adminpanel/exam/add/add-department.html", context)
    else:
        return redirect("admin_dashboard")
