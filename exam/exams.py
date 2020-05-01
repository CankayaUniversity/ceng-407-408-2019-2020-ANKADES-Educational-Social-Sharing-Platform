import datetime

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

from ankadescankaya.views import current_user_group, Categories
from exam.models import Department, School, Lecture


def add_exam(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == "moderator" or userGroup == "admin" or userGroup == "ogretmen":
        adding = "school"
        categories = Categories.all_categories()
        schools = School.objects.filter(isActive=True).order_by('slug')
        departments = Department.objects.filter(isActive=True).order_by('slug')
        lectures = Lecture.objects.filter(isActive=True).order_by('slug')
        adding = "school"
        if adding == "school":
            context = {
                "userGroup": userGroup,
                "departments": departments,
                "adding": adding,
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
            return render(request, "ankades/exam/add/choose-school.html", context)
        return redirect("add_exam")
    else:
        return redirect("index")
