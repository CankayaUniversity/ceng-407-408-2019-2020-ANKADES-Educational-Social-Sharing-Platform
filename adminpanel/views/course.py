import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from adminpanel.forms import CourseForm, CourseCategoryForm
from adminpanel.models import AdminActivity
from course.models import CourseCategory, Course


@login_required(login_url="login_admin")
def admin_courses(request):
    courses = Course.objects.all()
    context = {
        "courses": courses,
    }
    return render(request, "admin/course/all-courses.html", context)


@login_required(login_url="login_admin")
def admin_add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Kurs başarıyla eklendi !")
        return redirect("admin_courses")
    return render(request, "admin/course/add-course.html", context)


@login_required(login_url="login_admin")
def admin_edit_course(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Course, slug=slug)
        form = CourseForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Kurs başarıyla düzenlendi !")
            context = {
                "form": form,
            }
            return render(request, "admin/course/edit-course.html", context)
        return render(request, "admin/course/edit-course.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_course(request, slug):
    instance = get_object_or_404(Course, slug=slug)
    instance.delete()
    messages.success(request, "Kurs başarıyla silindi !")
    return redirect("admin_courses")


@login_required(login_url="login_admin")
def admin_course_category(request):
    course_categories_list = CourseCategory.objects.all()
    course_categories_limit = CourseCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "course_categories_list": course_categories_list,
        "course_categories_limit": course_categories_limit,
    }
    return render(request, "admin/course/all-categories.html", context)


@login_required(login_url="login_admin")
def admin_add_course_category(request):
    form = CourseCategoryForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Kurs kategorisi başarıyla eklendi !")
        return redirect("admin_index")
    return render(request, "admin/course/add-category.html", context)


@login_required(login_url="login_admin")
def admin_edit_course_category(request, slug):
    instance = get_object_or_404(CourseCategory, slug=slug)
    form = CourseCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Kurs kategorisi başarıyla düzenlendi !")
        return redirect("admin_index")
    return render(request, "admin/course/edit-category.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_course_category(request, slug):
    instance = get_object_or_404(CourseCategory, slug=slug)
    instance.delete()
    messages.success(request, "Kurs kategorisi başarıyla silindi !")
    return redirect("admin_index")
