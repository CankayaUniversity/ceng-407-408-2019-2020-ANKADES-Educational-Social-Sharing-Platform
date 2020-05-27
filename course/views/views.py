import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import DetailView

from account.models import AccountFollower
from account.views.views import get_user_follower, user_articles, user_questions, user_courses, user_exams
from adminpanel.views.article import ArticleCategoryView
from ankadescankaya.views.views import current_user_group, Categories
from article.models import ArticleCategory
from course.forms import CourseForm, CourseLectureFormSet, CourseSectionModelForm, SectionForm, LectureForm, VideoForm
from course.models import Course, CourseComment, CourseCategory, CourseSection, CourseLecture, CourseVideo
from question.models import QuestionComment


def all_courses(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    category = request.GET.getlist('c')
    sub = request.GET.getlist('s')
    lower = request.GET.getlist('l')
    getLowCategory = []
    articleCat = []
    topCategories = ArticleCategoryView.getTopCategory(request)
    articleComment = CourseComment.objects.filter(isActive=True)
    courses = Course.objects.filter(isActive=True)
    if category:
        top = CourseCategory.objects.filter(catNumber__in=category)
        sub = CourseCategory.objects.filter(isActive=True, parentId__catNumber__in=category)
        for getLower in sub:
            getLowCategory.append(getLower.catNumber)
        lower = CourseCategory.objects.filter(isActive=True, parentId__catNumber__in=getLowCategory)
        for cat in lower:
            articleCat.append(cat.catNumber)
        courses = Course.objects.filter(isActive=True, categoryId__catNumber__in=articleCat)
        context = {
            "userGroup": userGroup,
            "articleComment": articleComment,
            "category": category,
            "sub": sub,
            "top": top,
            "courses": courses,
            "courseCategories": categories[0],
            "courseSubCategories": categories[1],
            "courseLowerCategories": categories[2],
        }
        return render(request, "ankacademy/course/all-courses.html", context)
    if sub:
        subCat = CourseCategory.objects.filter(catNumber__in=sub)
        low = CourseCategory.objects.filter(isActive=True, parentId__catNumber__in=sub)
        for getLower in low:
            getLowCategory.append(getLower.catNumber)
        courses = Course.objects.filter(isActive=True, categoryId__catNumber__in=getLowCategory)
        context = {
            "userGroup": userGroup,
            "articleComment": articleComment,
            "category": category,
            "low": low,
            "subCat": subCat,
            "sub": sub,
            "courses": courses,
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankacademy/course/all-courses.html", context)
    if lower:
        lowCat = CourseCategory.objects.filter(catNumber__in=lower)
        courses = Course.objects.filter(isActive=True, categoryId__catNumber__in=lower)
        context = {
            "userGroup": userGroup,
            "articleComment": articleComment,
            "lowCat": lowCat,
            "lower": lower,
            "courses": courses,
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankacademy/course/all-courses.html", context)
    context = {
        "userGroup": userGroup,
        "topCategories": topCategories,
        "category": category,
        "courses": courses,
        "articleComment": articleComment,
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
    return render(request, "ankacademy/course/all-courses.html", context)


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
    categories = Categories.all_categories()
    courseForm = CourseForm(request.POST or None)
    sectionForm = SectionForm(request.POST or None)
    lectureForm = LectureForm(request.POST or None)
    videoForm = VideoForm(request.POST or None)
    courseCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    if request.method == "POST":
        new_course = Course()
        new_section = CourseSection()
        new_lecture = CourseLecture()
        new_course_video = CourseVideo()
        courseCategory = request.POST.get('courseCategory')
        courseTitle = request.POST.get('courseTitle')
        courseVideoTitle = request.POST.get('courseVideoTitle')
        #  COURSE
        if request.FILES:
            courseMedia = request.FILES.get('courseMedia')
            new_course.coursePicture = courseMedia
        if courseForm.is_valid():
            courseDescription = courseForm.cleaned_data.get("courseDescription")
            new_course.description = courseDescription
            courseIntroduction = courseForm.cleaned_data.get("courseIntroduction")
            new_course.introduction = courseIntroduction
        new_course.title = courseTitle
        new_course.creator = request.user
        new_course.createdDate = datetime.datetime.now()
        new_course.updatedDate = datetime.datetime.now()
        new_course.isActive = True
        new_course.categoryId_id = courseCategory
        new_course.courseNumber = get_random_string(length=32)
        new_course.save()
        #  SECTION
        sectionTitle = request.POST.get('sectionTitle')
        new_section.title = sectionTitle
        if sectionForm.is_valid():
            sectionDescription = sectionForm.cleaned_data.get("sectionDescription")
            new_section.description = sectionDescription
        new_section.isActive = True
        new_section.createdDate = datetime.datetime.now()
        new_section.updatedDate = datetime.datetime.now()
        new_section.courseId_id = new_course.id
        new_section.sectionNumber = get_random_string(length=32)
        new_section.save()
        #  LECTURE
        lectureTitle = request.POST.get('lectureTitle')
        new_lecture.title = lectureTitle
        if lectureForm.is_valid():
            lectureDescription = lectureForm.cleaned_data.get("lectureDescription")
            new_lecture.description = lectureDescription
        new_lecture.lectureNumber = get_random_string(length=32)
        new_lecture.createdDate = datetime.datetime.now()
        new_lecture.updatedDate = datetime.datetime.now()
        new_lecture.isActive = True
        new_lecture.sectionId_id = new_section.id
        new_lecture.save()
        # COURSE VIDEO
        lectureVideos = request.FILES.getlist('videos')
        courseVideoOwner = request.POST.get('courseVideoOwner')
        if lectureVideos:
            for vid in lectureVideos:
                new_course_video.media = vid
                new_course_video.lectureId_id = new_lecture.id
                new_course_video.createdDate = datetime.datetime.now()
                new_course_video.updatedDate = datetime.datetime.now()
                new_course_video.creator = request.user
                new_course_video.videoNumber = get_random_string(length=32)
                new_course_video.owner = courseVideoOwner
                new_course_video.isActive = True
                new_course_video.title = courseVideoTitle
                new_course_video.save()
        messages.success(request, "Kurs başarıyla oluşturuldu.")
        return redirect("all_courses")
    context = {
        "userGroup": userGroup,
        "courseCategory": courseCategory,
        "courseForm": courseForm,
        "sectionForm": sectionForm,
        "lectureForm": lectureForm,
        "videoForm": videoForm,
        "courseCategories": categories[0],
        "courseSubCategories": categories[1],
        "courseLowerCategories": categories[2],
    }
    return render(request, "ankacademy/course/add-course.html", context)


@login_required(login_url="login_account")
def add_section(request, courseNumber):
    """
    :param request:
    :param courseNumber:
    :return:
    """
    return None


# TODO
@login_required(login_url="login_account")
def add_lecture(request, courseNumber):
    """
    :param request:
    :param courseNumber:
    :return:
    """
    return None


def course_detail(request, slug, courseNumber):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = Course.objects.get(slug=slug, courseNumber=courseNumber)
        sections = CourseSection.objects.filter(courseId=instance).order_by('createdDate')
        lectures = CourseLecture.objects.filter(sectionId__courseId=instance).order_by('createdDate')
    except:
        messages.error(request, "Aradığınız kurs bulunamadı.")
        return redirect("404")
    currentUserEnrolled = False
    userGroup = current_user_group(request, request.user)
    existFollower = get_user_follower(request, request.user, instance.creator)
    articlesCount = user_articles(request, instance.creator).order_by('-createdDate__day')
    questionsCount = user_questions(request, instance.creator).order_by('-createdDate__day')
    coursesCount = user_courses(request, instance.creator).order_by('-createdDate__day')
    examsCount = user_exams(request, instance.creator)
    certifiedAnswersCount = QuestionComment.objects.filter(isCertified=True, isActive=True, creator=instance.creator)
    followers = AccountFollower.objects.filter(followingId__username=instance.creator)
    followings = AccountFollower.objects.filter(followerId__username=instance.creator)
    getFollowerForFollow = get_user_follower(request, request.user, followers)
    getFollowingForFollow = get_user_follower(request, request.user, followings)
    creatorGroup = current_user_group(request, instance.creator)
    instance.view += 1
    instance.save()
    if request.user in instance.enrolledAccount.all():
        currentUserEnrolled = True
    context = {
        "userGroup": userGroup,
        "existFollower": existFollower,
        "articlesCount": articlesCount,
        "questionsCount": questionsCount,
        "coursesCount": coursesCount,
        "examsCount": examsCount,
        "certifiedAnswersCount": certifiedAnswersCount,
        "followers": followers,
        "followings": followings,
        "getFollowerForFollow": getFollowerForFollow,
        "getFollowingForFollow": getFollowingForFollow,
        "creatorGroup": creatorGroup,
        "instance": instance,
        "sections": sections,
        "lectures": lectures,
        "currentUserEnrolled": currentUserEnrolled,
    }
    return render(request, "ankacademy/course/course-detail.html", context)


@login_required(login_url="login_account")
def course_lecture_detail(request, lectureNumber):
    """
    :param request:
    :param lectureNumber:
    """
    try:
        instance = CourseLecture.objects.get(lectureNumber=lectureNumber)
        section = CourseSection.objects.get(sectionNumber=instance.sectionId.sectionNumber)
        course = Course.objects.get(courseNumber=section.courseId.courseNumber)
    except:
        messages.error(request, "Aradığınız ders bulunamadı.")
        return redirect("404")
    if request.user in course.enrolledAccount.all():
        currentUserEnrolled = True
        sections = CourseSection.objects.filter(sectionNumber=instance.sectionId.sectionNumber)
        lectures = CourseLecture.objects.filter(sectionId=section)
        firstVideo = CourseVideo.objects.filter(isActive=True).first()
        userGroup = current_user_group(request, request)
        context = {
            "instance": instance,
            "section": section,
            "sections": sections,
            "lectures": lectures,
            "course": course,
            "currentUserEnrolled": currentUserEnrolled,
            "userGroup": userGroup,
            "firstVideo": firstVideo,
        }
        return render(request, "ankacademy/course/watch-course.html", context)
    else:
        return redirect("all_courses")


class CourseCategoryView(DetailView):

    @staticmethod
    def getTopCategory(request):
        """
        :param request:
        :return topCategory:
        """
        topCategory = CourseCategory.objects.filter(
            Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True) | Q(isRoot=True))
        return topCategory

    @staticmethod
    def getSubCategory(request, catNumber):
        """
        :param request:
        :param catNumber:
        :return subCategory:
        """
        instance = get_object_or_404(CourseCategory, catNumber=catNumber)
        subCategory = CourseCategory.objects.filter(parentId__catNumber=instance)
        return subCategory

    @staticmethod
    def getLowCategory(request, catNumber):
        """
        :param request:
        :return catNumber:
        """
        instance = get_object_or_404(CourseCategory, catNumber=catNumber)
        lowCategory = CourseCategory.objects.filter(parentId__catNumber=instance.catNumber)
        return lowCategory
