from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render

from account.views.views import current_user_group
from ankadescankaya.views import get_course_categories, get_course_sub_categories, get_course_lower_categories, \
    get_article_categories, get_article_sub_categories, get_article_lower_categories, get_question_categories, \
    get_question_sub_categories, get_question_lower_categories
from course.models import Course, CourseComment, CourseCategory


def all_courses(request):
    userGroup = current_user_group(request, request.user)
    courses_limit = Course.objects.filter(isActive=True).order_by('-createdDate')
    courseComment = CourseComment.objects.filter(isActive=True)
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    courseCategories = get_course_categories(request)
    courseSubCategories = get_course_sub_categories(request)
    courseLowerCategories = get_course_lower_categories(request)
    if keyword:
        courses = Course.objects.filter(Q(title__contains=keyword) | Q(creator=keyword) | Q(categoryId=keyword))
        context = {
            "courses": courses,
            "courseComment": courseComment,
            "courses_limit": courses_limit,
            "userGroup": userGroup,
            "courseCategories": courseCategories,
            "courseSubCategories": courseSubCategories,
            "courseLowerCategories": courseLowerCategories,
        }
        return render(request, "ankades/course/all-courses.html", context)
    else:
        courses = Course.objects.filter(isActive=True)
        paginator = Paginator(courses, 12)
        try:
            course_pagination = paginator.page(page)
        except PageNotAnInteger:
            course_pagination = paginator.page(1)
        except EmptyPage:
            course_pagination = paginator.page(paginator.num_pages)
        context = {
            "courses": courses,
            "courseComment": courseComment,
            "course_pagination": course_pagination,
            "courses_limit": courses_limit,
            "userGroup": userGroup,
            "courseCategories": courseCategories,
            "courseSubCategories": courseSubCategories,
            "courseLowerCategories": courseLowerCategories,
        }
    return render(request, "ankades/course/all-courses.html", context)


def course_category_page(request, slug):
    userGroup = current_user_group(request, request.user)
    articleCategories = get_article_categories(request)
    articleSubCategories = get_article_sub_categories(request)
    articleLowerCategories = get_article_lower_categories(request)
    questionCategories = get_question_categories(request)
    questionSubCategories = get_question_sub_categories(request)
    questionLowerCategories = get_question_lower_categories(request)
    courseCategories = get_course_categories(request)
    courseSubCategories = get_course_sub_categories(request)
    courseLowerCategories = get_course_lower_categories(request)
    try:
        courseCategory = CourseCategory.objects.get(slug=slug)
        courses = Course.objects.filter(categoryId=courseCategory)
        context = {
            "courseCategory": courseCategory,
            "courses": courses,
            "userGroup": userGroup,
            "articleCategories": articleCategories,
            "articleSubCategories": articleSubCategories,
            "articleLowerCategories": articleLowerCategories,
            "questionCategories": questionCategories,
            "questionSubCategories": questionSubCategories,
            "questionLowerCategories": questionLowerCategories,
            "courseCategories": courseCategories,
            "courseSubCategories": courseSubCategories,
            "courseLowerCategories": courseLowerCategories,
        }
        return render(request, "ankades/course/get-course-category.html", context)
    except:
        return render(request, "404.html")


def course_detail(request, slug):
    return None
