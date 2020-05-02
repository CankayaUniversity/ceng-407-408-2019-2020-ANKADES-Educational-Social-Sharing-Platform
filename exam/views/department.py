import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from ankadescankaya.views import current_user_group, Categories
from exam.models import Department, School


def all_departments(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = School.objects.get(slug=slug)
    except:
        messages.error(request, "Böyle bir okul bulunamadı.")
        return redirect("all_schools")
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    departments = Department.objects.filter(schoolId=instance, isActive=True)
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
    return render(request, "ankades/exam/all-departments.html", context)


def add_department(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == "moderator" or userGroup == "admin" or userGroup == "ogretmen":
        categories = Categories.all_categories()
        schools = School.objects.filter(isActive=True).order_by('slug')
        context = {
            "userGroup": userGroup,
            "schools": schools,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        if request.method == "POST":
            instance = Department()
            schoolId = request.POST["schoolId"]
            title = request.POST.get("title")
            check = Department.objects.filter(schoolId_id=schoolId, title=title)
            if check:
                messages.error(request, "Bu okula daha önce " + str(title) + " bölümü tanımlanmış.")
                return redirect("add_department")
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
        return render(request, "ankades/exam/add/add-department.html", context)
    else:
        return redirect("index")

