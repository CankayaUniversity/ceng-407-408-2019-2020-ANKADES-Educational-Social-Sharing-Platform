import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import AccountGroup
from adminpanel.forms import AdminCourseForm, AdminCourseCategoryForm
from adminpanel.models import AdminActivity
from course.models import CourseCategory, Course


@login_required(login_url="login_admin")
def admin_courses(request):
    """
    :param request:
    :return:
    """
    courses = Course.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "courses": courses,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/course/all-courses.html", context)


@login_required(login_url="login_admin")
def admin_add_course(request):
    """
    :param request:
    :return:
    """
    form = AdminCourseForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(
        Q(userId__username=request.user.username, groupId__slug="admin"))
    context = {
        "form": form,
        "adminGroup": adminGroup
    }
    if form.is_valid():
        categoryId = form.cleaned_data.get("categoryId")
        title = form.cleaned_data.get("title")
        slug = form.cleaned_data.get("slug")
        description = form.cleaned_data.get("description")
        media = form.cleaned_data.get("media")
        isActive = form.cleaned_data.get("isActive")
        isPrivate = form.cleaned_data.get("isPrivate")
        adminAddedCourse = Course(categoryId=categoryId, title=title, slug=slug, description=description, media=media,
                                  isActive=isActive, isPrivate=isPrivate)
        adminAddedCourse.creator = request.user.username
        adminAddedCourse.save()
        messages.success(request, "Kurs başarıyla eklendi !")
        return redirect("admin_courses")
    return render(request, "admin/course/add-course.html", context)


#Yeni Form yapısı ile yapılacak
@login_required(login_url="login_admin")
def admin_edit_course(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    if request.user.is_authenticated:
        instance = get_object_or_404(Course, slug=slug)
        form = AdminCourseForm(request.POST or None, request.FILES or None, instance=instance)
        adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Kurs başarıyla düzenlendi !")
            context = {
                "form": form,
                "adminGroup": adminGroup,
            }
            return render(request, "admin/course/edit-course.html", context)
        return render(request, "admin/course/edit-course.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_course(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Course, slug=slug)
    if instance.isActive is True:
        instance.isActive = False
        messages.success(request, "Kurs başarıyla silindi !")
        return redirect("admin_courses")
    else:
        messages.error(request, "Kurs zaten aktif değil!")
        return redirect("admin_courses")


#Yeni Form yapısı ile yapılacak
@login_required(login_url="login_admin")
def admin_course_category(request):
    """
    :param request:
    :return:
    """
    course_categories_list = CourseCategory.objects.all()
    course_categories_limit = CourseCategory.objects.all().order_by('-createdDate')[:5]
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "course_categories_list": course_categories_list,
        "course_categories_limit": course_categories_limit,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/course/all-categories.html", context)


#Yeni Form yapısı ile yapılacak
@login_required(login_url="login_admin")
def admin_add_course_category(request):
    """
    :param request:
    :return:
    """
    form = AdminCourseCategoryForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "form": form,
        "adminGroup": adminGroup,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user.username
        instance.save()
        messages.success(request, "Kurs kategorisi başarıyla eklendi !")
        return redirect("admin_index")
    return render(request, "admin/course/add-category.html", context)


#Yeni Form yapısı ile yapılacak
@login_required(login_url="login_admin")
def admin_edit_course_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(CourseCategory, slug=slug)
    form = AdminCourseCategoryForm(request.POST or None, instance=instance)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "form": form,
        "adminGroup": adminGroup,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Kurs kategorisi başarıyla düzenlendi !")
        return redirect("admin_edit_course_category")
    return render(request, "admin/course/edit-category.html", context)


@login_required(login_url="login_admin")
def admin_delete_course_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(CourseCategory, slug=slug)
    if instance.isActive is True:
        instance.isActive = False
        messages.success(request, "Kurs kategorisi başarıyla etkisizleştirildi !")
        return redirect("admin_course_category")
    else:
        messages.error(request, "Kurs kategorisi zaten aktif değil!")
        return redirect("admin_course_category")