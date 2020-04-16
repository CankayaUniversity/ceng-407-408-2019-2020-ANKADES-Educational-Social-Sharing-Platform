from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from ankadescankaya.views import current_user_group
from ankadescankaya.views import Categories
from article.models import ArticleCategory
from exam.models import School, Exam
from question.models import QuestionCategory


def all_schools(request):
    schools = School.objects.filter(isActive=True)
    userGroup = current_user_group(request, request.user)
    exams = Exam.objects.filter(isActive=True)
    categories = Categories.all_categories()
    context = {
        "schools": schools,
        "exams": exams,
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
    return redirect("404")
