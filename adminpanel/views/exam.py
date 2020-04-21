import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from ankadescankaya.views import current_user_group, Categories
from exam.models import ExamCategory


def admin_add_school(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
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
    }
    if request.method == "POST":
        instance = ExamCategory()
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        instance.title = title
        instance.slug = slug
        instance.isActive = True
        instance.creator = request.user
        instance.createdDate = datetime.datetime.now()
        instance.updatedDate = datetime.datetime.now()
        instance.isRoot = True
        instance.parentId_id = instance.id
        instance.isSchool = True
        instance.save()
        messages.success(request, "Okul başarıyla eklendi.")
        return redirect("admin_add_school")
    return render(request, "adminpanel/exam/add-school.html", context)


def admin_all_schools(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    schools = ExamCategory.objects.filter(isSchool=True).order_by('title')
    departments = ExamCategory.objects.filter(isDepartment=True).order_by('title')
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
        "departments": departments,
    }
    return render(request, "adminpanel/exam/all-schools.html", context)