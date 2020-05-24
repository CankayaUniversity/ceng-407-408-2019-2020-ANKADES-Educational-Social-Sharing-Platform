from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from account.models import AccountGroup
from adminpanel.models import SiteSettings
from ankadescankaya.views.search import SearchKeyword
from article.models import ArticleCategory
from course.models import CourseCategory
from question.models import QuestionCategory


class Categories(DetailView):
    @staticmethod
    def all_categories():
        """
        :return:
        """
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
    :rtype:
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
    """
    :param request:
    :return:
    """
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


def terms_of_use(request):
    """"
    :param request:
    :return:
    """
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
    try:
        instance = SiteSettings.objects.get(slug="terms-of-use")
    except:
        return redirect("404")
    context = {
        "userGroup": userGroup,
        "instance": instance,
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
    return render(request, "ankacademy/terms-of-use.html", context)


def privacy_policy(request):
    """
    :param request:
    :return:
    """
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
    try:
        instance = SiteSettings.objects.get(slug="privacy-policy")
    except:
        return redirect("404")
    context = {
        "userGroup": userGroup,
        "instance": instance,
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
    return render(request, "ankacademy/privacy-policy.html", context)


def search_keyword(request):
    """
    :param request:
    :return:
    """
    articles = SearchKeyword.search_article(request)
    questions = SearchKeyword.search_question(request)
    courses = SearchKeyword.search_course(request)
    schools = SearchKeyword.search_school(request)
    lectures = SearchKeyword.search_lecture(request)
    exams = SearchKeyword.search_exam(request)
    accounts = SearchKeyword.search_account(request)
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "articles": articles,
        "questions": questions,
        "courses": courses,
        "schools": schools,
        "lectures": lectures,
        "exams": exams,
        "accounts": accounts,
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
    return render(request, "ankades/search.html", context)
