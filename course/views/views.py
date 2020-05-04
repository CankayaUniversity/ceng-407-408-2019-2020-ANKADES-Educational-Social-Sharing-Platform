import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string

from ankadescankaya.views import Categories
from ankadescankaya.views import current_user_group
from course.forms import CourseForm, CourseLectureFormSet, CourseSectionModelForm
from course.models import Course, CourseComment, CourseCategory


def all_courses(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    courses_limit = Course.objects.filter(isActive=True).order_by('-createdDate')
    courseComment = CourseComment.objects.filter(isActive=True)
    page = request.GET.get('page', 1)
    categories = Categories.all_categories()
    keyword = request.GET.get("keyword")
    if keyword:
        courses = Course.objects.filter(
            Q(title__contains=keyword, isActive=True) | Q(creator=keyword, isActive=True) | Q(categoryId=keyword,
                                                                                              isActive=True))
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
            "userGroup": userGroup,
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


# TODO
# Yönlendirme yapılacak -> Bölüm Ekle
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
        # return redirect(reverse("add_section", kwargs={"courseNumber": instance.courseNumber}))
        return redirect(request, "add_section", instance.courseNumber)
    return render(request, "ankades/course/add-course.html", context)


@login_required(login_url="login_account")
def add_section(request, courseNumber):
    lectureformset = None
    sectionform = None
    getCourse = get_object_or_404(Course, courseNumber=courseNumber)
    userGroup = current_user_group(request, request.user)
    courseCategory = CourseCategory.objects.filter(Q(isActive=True, isCategory=False))
    categories = Categories.all_categories()
    if request.method == 'GET':
        sectionform = CourseSectionModelForm(request.GET or None)
        lectureformset = CourseLectureFormSet()
    elif request.method == 'POST':
        sectionform = CourseSectionModelForm(request.POST)
        lectureformset = CourseLectureFormSet(request.POST)
        if sectionform.is_valid() and lectureformset.is_valid():
            section = sectionform.save(commit=False)
            section.title = sectionform.cleaned_data.get("title")
            section.courseId = getCourse
            section.save()

            for form in lectureformset:
                lecture = form.save(commit=False)
                lecture.sectionId = section
                lecture.save()
            return redirect(reverse("add_section", kwargs={"courseNumber": courseNumber}))
    context = {
        "courseCategory": courseCategory,
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
        "lectureformset": lectureformset,
        "sectionform": sectionform,
    }
    return render(request, "ankades/course/add-section.html", context)


# TODO
@login_required(login_url="login_account")
def add_lecture(request, courseNumber):
    return None


# TODO
def course_detail(request, slug):
    return None
