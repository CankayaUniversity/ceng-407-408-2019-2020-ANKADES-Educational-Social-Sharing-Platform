import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from ankadescankaya.views import current_user_group
from ankadescankaya.views import Categories
from course.forms import CourseForm
from course.models import Course, CourseComment, CourseCategory


def all_courses(request):
    userGroup = current_user_group(request, request.user)
    courses_limit = Course.objects.filter(isActive=True).order_by('-createdDate')
    courseComment = CourseComment.objects.filter(isActive=True)
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    categories = Categories.all_categories()
    if keyword:
        courses = Course.objects.filter(Q(title__contains=keyword, isActive=True) | Q(creator=keyword, isActive=True) | Q(categoryId=keyword, isActive=Tru))
        context = {
            "courses": courses,
            "courseComment": courseComment,
            "courses_limit": courses_limit,
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
    return render(request, "ankades/course/all-courses.html", context)


def course_category_page(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        courseCategory = CourseCategory.objects.get(slug=slug)
        courses = Course.objects.filter(categoryId=courseCategory)
        context = {
            "courseCategory": courseCategory,
            "courses": courses,
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
        return render(request, "ankades/course/get-course-category.html", context)
    except:
        return redirect("404")


@login_required(login_url="login_account")
def add_course(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    courseCategory = CourseCategory.objects.filter(Q(isActive=True, isCategory=False))
    form = CourseForm(request.POST or None)
    categories = Categories.all_categories()
    context = {
        "courseCategory": courseCategory,
        "userGroup": userGroup,
        "form": form,
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
    if request.method == "POST":
        value = request.POST['categoryId']
        title = request.POST.get("title")
        introduction = request.POST.get("introduction")
        isPrivate = request.POST.get("isPrivate") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
        if not title and description:
            messages.error(request, "Kategori, Başlık ve Açıklama kısımları boş geçilemez")
            return render(request, "ankades/course/add-course.html", context)
        instance = Course(title=title, description=description, introduction=introduction, isPrivate=isPrivate)
        if request.FILES:
            coursePicture = request.FILES.get('coursePicture')
            fs = FileSystemStorage()
            fs.save(coursePicture.name, coursePicture)
            instance.coursePicture = coursePicture
        instance.creator = request.user
        instance.courseNumber = get_random_string(length=32)
        instance.isActive = False
        instance.categoryId_id = value
        instance.save()
        messages.success(request, "Kurs başarıyla eklendi.")
        return redirect("index")
    return render(request, "ankades/course/add-course.html", context)


@login_required(login_url="login_account")
def add_section(request, courseNumber):
    return None


@login_required(login_url="login_account")
def add_lecture(request, courseNumber):
    return None


def course_detail(request, slug):
    return None
