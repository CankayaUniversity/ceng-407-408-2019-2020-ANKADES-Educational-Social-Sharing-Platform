from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from article.models import ArticleCategory
from exam.models import School, Exam
from question.models import QuestionCategory


def all_schools(request):
    schools = School.objects.all()
    exams = Exam.objects.all()
    articleCategories = ArticleCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    context = {
        "schools": schools,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
    }
    return render(request, "ankades/../../templates/test/exam/all-schools.html", context)
