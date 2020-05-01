import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from ankadescankaya.views import current_user_group, Categories
from exam.models import School, Department


def admin_all_schools(request):
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
    return render(request, "adminpanel/exam/add-school.html", context)


def admin_add_department(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    schools = School.objects.filter(isActive=True).order_by('slug')
    context = {
        "userGroup": userGroup,
        "schools": schools,
    }
    if request.method == "POST":
        instance = Department()
        schoolId = request.POST["schoolId"]
        title = request.POST.get("title")
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
    return render(request, "adminpanel/exam/add-department.html", context)


def admin_add_lecture(request, departmentCode):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    departmentCode = departmentCode
    try:
        department = Department.objects.get(departmentCode=departmentCode)
    except:
        messages.error(request, "Bölüm Bulanamadı.")
        # TODO should change index to all departments
        return redirect("index")
    context = {
        "userGroup": userGroup,
        "department": department,
    }
    if request.method == "POST":
        instance = Department()
        schoolId = request.POST["schoolId"]
        title = request.POST.get("title")
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
    return render(request, "adminpanel/exam/add-department.html", context)


def admin_all_schools(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    schools = School.objects.filter().order_by('slug')
    departments = Department.objects.filter().order_by('slug')
    context = {
        "userGroup": userGroup,
        "schools": schools,
        "departments": departments,
    }
    return render(request, "adminpanel/exam/all-schools.html", context)