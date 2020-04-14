from django.db.models import Q

from article.models import ArticleCategory
from course.models import CourseCategory
from question.models import QuestionCategory


def get_article_categories(request):
    articleCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    return articleCategories


def get_article_sub_categories(request):
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    return articleSubCategories


def get_article_lower_categories(request):
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    return articleLowerCategories


def get_question_categories(request):
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    return questionCategories


def get_question_sub_categories(request):
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    return questionSubCategories


def get_question_lower_categories(request):
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    return questionLowerCategories


def get_course_categories(request):
    courseCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    return courseCategories


def get_course_sub_categories(request):
    courseSubCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    return courseSubCategories


def get_course_lower_categories(request):
    courseLowerCategories = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    return courseLowerCategories
