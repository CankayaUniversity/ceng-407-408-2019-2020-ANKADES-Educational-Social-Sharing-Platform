import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from ankadescankaya.views import current_user_group, Categories
from exam.models import Department, School


def all_schools(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    schools = School.objects.filter(isActive=True).order_by('title')
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
