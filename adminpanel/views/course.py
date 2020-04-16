import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from account.models import AccountGroup
from ankadescankaya.views import current_user_group
from adminpanel.models import AdminLogs
from course.models import Course
from course.models import CourseCategory, Course


@login_required(login_url="login_admin")
def admin_add_course_category(request):
    """
    :param request:
    :return:
    """
    courseCategory = CourseCategory.objects.filter(Q(isActive=True, isCategory=True))
    userGroup = current_user_group(request, request.user)
    activity = AdminLogs()
    context = {
        "userGroup": userGroup,
        "courseCategory": courseCategory,
    }
    if userGroup == 'admin':
        if request.method == "POST":
            categoryId = request.POST["categoryId"]
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == "on"
            isCategory = request.POST.get("isCategory") == "on"
            try:
                getTitle = CourseCategory.objects.get(title=title)
                if title:
                    error = title + " isimli kategori " + getTitle.parentId.title + " kategorisinde zaten mevcut."
                    messages.error(request, error)
                    return redirect("admin_add_course_category")
            except:
                instance = CourseCategory(title=title, isActive=isActive,
                                            isCategory=isCategory)
                instance.creator = request.user
                instance.parentId_id = categoryId
                instance.save()
                activity.title = "Kurs Kategorisi Ekleme: " + str(request.user)
                activity.application = "Course"
                activity.createdDate = datetime.datetime.now()
                activity.method = "POST"
                activity.creator = request.user.username
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kurslar için kategori ekledi."
                activity.save()
                messages.success(request, "Kurs kategorisi başarıyla eklendi !")
                return redirect("admin_course_categories")
        return render(request, "adminpanel/course/add-course-category.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_dashboard")


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
        activity = AdminLogs()
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.save()
                activity.title = "Kurs Aktifleştirme"
                activity.application = "Course"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = request.user.username
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kurs aktifliğini kaldırdı."
                activity.save()
                messages.success(request, "Kurs kategorisi artık aktif değil.")
                return redirect("admin_all_courses")
            else:
                instance.isActive = True
                instance.save()
                activity.title = "Kurs Aktifleştirme"
                activity.application = "Course"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = request.user.username
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kurs aktifleştirdi."
                activity.save()
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
        activity = AdminLogs()
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.save()
                activity.title = "Kurs Kategorisini Aktifleştirme"
                activity.application = "Course"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = request.user.username
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kurs kategorisinin aktifliğini kaldırdı."
                activity.save()
                messages.success(request, "Kurs kategorisi artık aktif değil.")
                return redirect("admin_course_categories")
            else:
                instance.isActive = True
                instance.save()
                activity.title = "Kurs Kategorisini Aktifleştirme"
                activity.application = "Course"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = request.user.username
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kurs kategorisinin aktifleştirdi."
                activity.save()
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
    activity = AdminLogs()
    if userGroup == 'admin':
        instance = get_object_or_404(Course, slug=slug)
        if instance.isActive is True:
            activity.title = "Kurs Silme"
            activity.application = "Course"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = request.user.username
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı kurs silme işleminde bulundu. Başarısız."
            activity.save()
            messages.error(request, "Kurs aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_course_categories")
        else:
            instance.delete()
            activity.title = "Kurs Silme"
            activity.application = "Course"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = request.user.username
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı kurs sildi."
            activity.save()
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
    activity = AdminLogs()
    if userGroup == 'admin':
        instance = get_object_or_404(CourseCategory, slug=slug)
        if instance.isActive is True:
            activity.title = "Kurs Kategori Silme"
            activity.application = "Course"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = request.user.username
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı kurs kategorisini silme işleminde bulundu. Başarısız."
            activity.save()
            messages.error(request, "Kurs kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_course_categories")
        else:
            instance.delete()
            activity.title = "Kurs Kategori Silme"
            activity.application = "Course"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = request.user.username
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı kurs kategorisini sildi."
            activity.save()
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

