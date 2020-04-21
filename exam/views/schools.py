from django.shortcuts import render

from ankadescankaya.views import current_user_group, Categories
from exam.models import ExamCategory


def all_schools(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    schools = ExamCategory.objects.filter(isActive=True, isSchool=True).order_by('title')
    departments = ExamCategory.objects.filter(isActive=True, isDepartment=True).order_by('title')
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
    return render(request, "ankades/exam/all-schools.html", context)
