from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView

from account.models import AccountGroup
from article.models import ArticleCategory
from course.models import CourseCategory
from exam.models import ExamCategory
from question.models import QuestionCategory


class Categories(DetailView):

    @staticmethod
    def all_categories():
        articleCategories = ArticleCategory.objects.filter(
            Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
        articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
        articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
        questionCategories = QuestionCategory.objects.filter(
            Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
        questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
        questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
        courseCategories = CourseCategory.objects.filter(
            Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
        courseSubCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
        courseLowerCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
        return [
            articleCategories, articleSubCategories, articleLowerCategories,
            questionCategories, questionSubCategories, questionLowerCategories,
            courseCategories, courseSubCategories, courseLowerCategories
        ]


def current_user_group(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        group = AccountGroup.objects.get(userId__username=username)
        return str(group.groupId)
    except:
        group = None
        return group


def get_404(request):
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
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
    return render(request, "404.html", context)