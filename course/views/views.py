from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from course.forms import AddArticleComment
from course.models import Course, CourseCategory, CourseComment


# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all().order_by('-course_created_date')
#     serializer_class = CourseSerializer
#
#
# class CourseCategoryViewSet(viewsets.ModelViewSet):
#     queryset = CourseCategory.objects.all()
#     serializer_class = CourseCategorySerializer
#
#
# class CourseSubToSubCategoryViewSet(viewsets.ModelViewSet):
#     queryset = CourseSubToSubCategory.objects.all().order_by('-course_sub_to_sub_category_created_date')
#     serializer_class = CourseSubToSubCategorySerializer


def all_courses(request):
    keyword = request.GET.get("keyword")
    if keyword:
        coursePagination = Course.objects.filter(Q(title__contains=keyword) |
                                                 Q(content__contains=keyword))
        context = {
            "coursePagination": coursePagination,
        }
        return render(request, "ankades/../templates/test/course/courses.html", context)

    courses = Course.objects.all()
    courseComments = CourseComment.objects.all()
    courseLimit = Course.objects.all().order_by('-id')[:10]
    courseCategories = CourseCategory.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(courses, 10)
    try:
        article_pagination = paginator.page(page)
    except PageNotAnInteger:
        article_pagination = paginator.page(1)
    except EmptyPage:
        article_pagination = paginator.page(paginator.num_pages)

    context = {
        "courses": courses,
        "courseComments": courseComments,
        "courseCategories": courseCategories,
        "courseLimit": courseLimit,
    }
    return render(request, "ankades/../templates/test/course/courses.html", context)


def course_categories(request):
    keyword = request.GET.get("keyword")
    if keyword:
        searchCategories = CourseCategory.objects.filter(title__contains=keyword)
        return render(request, "ankades/../templates/test/course/courses.html", {"searchCategories": searchCategories})
    categories = CourseCategory.objects.all()
    return render(request, "ankades/../templates/test/course/courses.html", {"categories": categories})


def course_detail(request, slug):
    courseDetail = get_object_or_404(Course, slug=slug)
    courses = Course.objects.all()
    courseComments = CourseComment.objects.all()
    courseCategories = CourseCategory.objects.all()
    courseDetail.view += 1
    context = {
        "articleDetail": courseDetail,
        "courses": courses,
        "courseComments": courseComments,
        "courseCategories": courseCategories,
    }
    return render(request, "ankades/../templates/test/course/course-detail.html", context)
