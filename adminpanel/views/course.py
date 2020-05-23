import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.generic import DetailView

from ankadescankaya.views.views import current_user_group
from course.models import CourseCategory, Course


@login_required(login_url="login_admin")
def admin_add_course_category(request):
    """
    :param request:
    :return:
    """
    topCategory = CourseCategoryView.getTopCategory(request)
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
        "topCategory": topCategory
    }
    if userGroup == 'admin' or userGroup == 'moderator':
        getTop = request.GET.get('getTop')
        postTop = request.POST.get('postTop')
        home = request.POST.get('home')
        if getTop or home or postTop:
            if home:  # If request category slug is equal to home
                parent = CourseCategory.objects.get(catNumber=home)
                if request.method == 'POST':
                    title = request.POST.get('title')
                    isActive = request.POST.get("isActive") == 'on'
                    new_cat = CourseCategory(creator=request.user, isCategory=True, isActive=isActive, isRoot=False,
                                              parentId=parent, title=title)
                    new_cat.catNumber = "cc-" + get_random_string(length=6)
                    new_cat.createdDate = datetime.datetime.now()
                    new_cat.creator = request.user
                    new_cat.save()
                    messages.success(request, "Kurs için üst kategori başarıyla eklendi.")
                    return redirect("admin_add_course_category")
            if getTop == 'cc-rochVWt':
                home = CourseCategory.objects.get(catNumber=getTop)
                context = {
                    "getTop": getTop,
                    "userGroup": userGroup,
                    "home": home
                }
                return render(request, "adminpanel/course/add-course-category.html", context)
            if postTop:
                inputTop = CourseCategory.objects.get(catNumber=postTop)
                selectSub = CourseCategory.objects.filter(parentId=inputTop)
                context = {
                    "getTop": getTop,
                    "inputTop": inputTop,
                    "selectSub": selectSub,
                    "userGroup": userGroup,
                }
                if request.method == 'POST':
                    selection = request.POST.get('selection')
                    if selection == 'none':
                        title = request.POST.get('title')
                        isActive = request.POST.get("isActive") == 'on'
                        new_top = CourseCategory(title=title, isCategory=True, isActive=isActive, isRoot=False,
                                                  parentId=inputTop)
                        new_top.catNumber = "cc-" + get_random_string(length=6)
                        new_top.createdDate = datetime.datetime.now()
                        new_top.creator = request.user
                        new_top.save()
                        messages.success(request, "Alt kategori başarıyla eklendi.")
                        return redirect("admin_add_course_category")
                    else:
                        title = request.POST.get('title')
                        isActive = request.POST.get("isActive") == 'on'
                        new_lower = CourseCategory(title=title, isCategory=True, isActive=isActive, isRoot=False,
                                                    parentId=inputTop)
                        new_lower.catNumber = "cc-" + get_random_string(length=6)
                        new_lower.createdDate = datetime.datetime.now()
                        new_lower.creator = request.user
                        new_lower.save()
                        messages.success(request, "En alt kategori başarıyla eklendi.")
                        return redirect("admin_add_course_category")
                return render(request, "adminpanel/course/add-course-category.html", context)
            else:
                inputTop = CourseCategory.objects.get(catNumber=getTop)
                selectSub = CourseCategory.objects.filter(parentId=inputTop)
                context = {
                    "getTop": getTop,
                    "inputTop": inputTop,
                    "selectSub": selectSub,
                    "userGroup": userGroup,
                }
                return render(request, "adminpanel/course/add-course-category.html", context)
        else:
            return render(request, "adminpanel/course/add-course-category.html", context)
    else:
        return redirect("index")


@login_required(login_url="login_admin")
def admin_course_categories(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = CourseCategory.objects.all()
    courseCategory = CourseCategory.objects.filter(Q(isActive=True, isCategory=True))
    courseCategoryLimit = CourseCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "courseCategory": courseCategory,
        "courseCategoryLimit": courseCategoryLimit,
    }
    return render(request, "adminpanel/course/categories.html", context)


@login_required(login_url="login_admin")
def admin_delete_course_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = CourseCategory.objects.get(slug=slug)
        if instance.isActive is True:
            messages.error(request, "Kurs kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_course_categories")
        else:
            instance.delete()
            messages.success(request, "Kurs kategorisi başarıyla silindi.")
            return redirect("admin_course_categories")
    except:
        return render(request, "adminpanel/404-admin.html")


@login_required(login_url="login_admin")
def admin_isactive_course(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = Course.objects.get(slug=slug)
        userGroup = current_user_group(request, request.user)
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Kurs kategorisi artık aktif değil.")
                return redirect("admin_all_courses")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Kurs başarıyla aktifleştirildi.")
                return redirect("admin_all_courses")
        else:
            messages.error(request, "Yetkiniz Yok")
            return redirect("admin_all_courses")
    except:
        return render(request, "adminpanel/404-admin.html")


@login_required(login_url="login_admin")
def admin_isactive_course_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = CourseCategory.objects.get(slug=slug)
        userGroup = current_user_group(request, request.user)
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Kurs kategorisi artık aktif değil.")
                return redirect("admin_course_categories")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Kurs kategorisi başarıyla aktifleştirildi.")
                return redirect("admin_course_categories")
        else:
            messages.error(request, "Yetkiniz Yok")
            return redirect("admin_course_categories")
    except:
        return render(request, "adminpanel/404-admin.html")


@login_required(login_url="login_admin")
def admin_delete_course(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        instance = get_object_or_404(Course, slug=slug)
        if instance.isActive is True:
            messages.error(request, "Kurs aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_course_categories")
        else:
            instance.delete()
            messages.success(request, "Kurs başarıyla silindi.")
            return redirect("admin_all_courses")
    else:
        messages.error(request, "Yetkiniz Yok")
        return redirect("admin_all_courses")


@login_required(login_url="login_admin")
def admin_delete_course_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        instance = get_object_or_404(CourseCategory, slug=slug)
        if instance.isActive is True:
            messages.error(request, "Kurs kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_course_categories")
        else:
            instance.delete()
            messages.success(request, "kurs kategorisi başarıyla silindi.")
            return redirect("admin_course_categories")
    else:
        messages.error(request, "Yetkiniz Yok")
        return redirect("admin_course_categories")


@login_required(login_url="login_admin")
def admin_all_courses(request):
    """
    :param request:
    :return:
    """
    courses = Course.objects.all()
    userGroup = current_user_group(request, request.user)
    context = {
        "courses": courses,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/course/all-courses.html", context)


class CourseCategoryView(DetailView):

    @staticmethod
    @login_required(login_url="login_admin")
    def getTopCategory(request):
        """
        :param request:
        :return topCategory:
        """
        topCategory = CourseCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True)|Q(isRoot=True))
        return topCategory

    @staticmethod
    @login_required(login_url="login_admin")
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
    @login_required(login_url="login_admin")
    def getLowCategory(request, catNumber):
        """
        :param request:
        :return catNumber:
        """
        instance = get_object_or_404(CourseCategory, catNumber=catNumber)
        lowCategory = CourseCategory.objects.filter(parentId__catNumber=instance)
        return lowCategory