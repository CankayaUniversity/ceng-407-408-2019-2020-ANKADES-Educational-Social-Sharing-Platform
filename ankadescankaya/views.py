from django.db.models import Q

from article.models import ArticleCategory
from course.models import CourseCategory
from question.models import QuestionCategory


def get_article_categories(request):
    """
    :param request:
    :return:
    """
    articleCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    return articleCategories


def get_article_sub_categories(request):
    """
    :param request:
    :return:
    """
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    return articleSubCategories


def get_article_lower_categories(request):
    """
    :param request:
    :return:
    """
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    return articleLowerCategories


def get_question_categories(request):
    """
    :param request:
    :return:
    """
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    return questionCategories


def get_question_sub_categories(request):
    """
    :param request:
    :return:
    """
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    return questionSubCategories


def get_question_lower_categories(request):
    """
    :param request:
    :return:
    """
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    return questionLowerCategories


def get_course_categories(request):
    """
    :param request:
    :return:
    """
    courseCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    return courseCategories


def get_course_sub_categories(request):
    """
    :param request:
    :return:
    """
    courseSubCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    return courseSubCategories


def get_course_lower_categories(request):
    """
    :param request:
    :return:
    """
    courseLowerCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    return courseLowerCategories
