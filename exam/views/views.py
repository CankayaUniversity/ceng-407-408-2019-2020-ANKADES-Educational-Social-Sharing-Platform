from django.shortcuts import render, redirect

from ankadescankaya.views import current_user_group, Categories
from exam.models import ExamCategory


def all_departments(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        getParent = ExamCategory.objects.get(slug=slug)
    except:
        return redirect("404")
    departments = ExamCategory.objects.filter(parentId=getParent, isActive=True, isDepartment=True)
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
        "getParent": getParent,
        "departments": departments,
    }
    return render(request, "ankades/exam/all-departments.html", context)