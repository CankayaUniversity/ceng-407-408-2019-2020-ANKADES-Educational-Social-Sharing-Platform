import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from ankadescankaya.views import current_user_group, Categories
from exam.models import School, Department


def all_schools(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    schools = Department.objects.filter(isActive=True, schoolId_id__isnull=False).order_by('title')
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
        "schools": schools,
    }
    return render(request, "ankades/exam/all-schools.html", context)


def all_departments(request, slug):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        departments = Department.objects.get(schoolId=slug, isActive=True)
    except:
        messages.error(request, "Okula ait bölümler bulunamadı.")
        return redirect("all_schools")
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
        "departments": departments,
    }
    return render(request, "ankades/exam/all-schools.html", context)


def add_department(request):
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
