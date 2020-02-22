from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from adminpanel.forms import CourseCategoryForm, CourseSubCategoryForm, CourseSubToSubCategoryForm, CourseForm
from adminpanel.models import AdminActivity
from course.models import CourseCategory, CourseSubCategory, CourseSubToSubCategory, Course


@login_required(login_url="login_admin")
def admin_courses(request):
    keyword = request.GET.get("keyword")
    if keyword:
        search_course = Course.objects.filter(
            Q(course_title__contains=keyword) |
            Q(course_content__contains=keyword) |
            Q(course_author_id__contains=keyword) |
            Q(course_created_date__contains=keyword) | Q(course_sub_to_sub_category_id__contains=keyword))
        context = {
            "search_course": search_course,
        }
        return render(request, "admin/course/all-courses.html", context)

    course_list = Course.objects.all()
    course_limit = Course.objects.all().order_by('-course_created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(course_limit, 5)
    try:
        course_pagination = paginator.page(page)
    except PageNotAnInteger:
        course_pagination = paginator.page(1)
    except EmptyPage:
        course_pagination = paginator.page(paginator.num_pages)

    context = {
        "course_list": course_list,
        "course_pagination": course_pagination,
        "course_limit": course_limit,
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
        instance.course_author = request.user
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_author
        act.act_title = "Kurs Eklendi: " + form.cleaned_data.get("course_title")
        act.act_created_date = instance.course_created_date
        act.act_method = "PUT"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_content")
        act.save()
        return redirect("course_table")
    return render(request, "admin/course/add-course.html", context)


@login_required(login_url="login_admin")
def admin_edit_course(request, course_slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Course, course_slug=course_slug)
        form = CourseForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.course_author = request.user
            instance.save()
            act = AdminActivity()
            act.act_creator = instance.course_author
            act.act_title = "Kurs Düzenlendi: " + form.cleaned_data.get("course_title")
            act.act_created_date = instance.course_created_date
            act.act_method = "PUT"
            act.act_app = "Kurs"
            act.act_desc = "Açıklama: " + form.cleaned_data.get("course_content")
            act.save()
            context = {
                "form": form,
                "act.act_creator": act.act_creator,
                "act.act_title": act.act_title,
                "act.act_created_date": act.act_created_date,
                "act.act_method": act.act_method,
                "act.act_app": act.act_app,
                "act.act_desc": act.act_desc,
            }
            return render(request, "admin/course/edit-course.html", context)
        return render(request, "admin/course/edit-course.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_course(request, course_slug):
    instance = get_object_or_404(Course, course_slug=course_slug)
    instance.delete()
    return redirect("course_category")


@login_required(login_url="login_admin")
def admin_course_category(request):
    keyword = request.GET.get("keyword")
    if keyword:
        course_categories_pagination = CourseCategory.objects.filter(
            Q(id__contains=keyword) |
            Q(course_category_title__contains=keyword) |
            Q(course_category_created_date__contains=keyword) |
            Q(course_category_slug__contains=keyword) | Q(course_category_id__contains=keyword))
        context = {
            "course_categories_pagination": course_categories_pagination,
        }
        return render(request, "admin/course/all-categories.html", context)
    course_categories_list = CourseCategory.objects.all()
    course_sub_categories_list = CourseSubCategory.objects.all()
    course_sub_to_sub_categories_list = CourseSubToSubCategory.objects.all()
    course_categories_limit = CourseCategory.objects.all().order_by('-course_category_created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(course_categories_limit, 5)
    try:
        course_categories_pagination = paginator.page(page)
    except PageNotAnInteger:
        course_categories_pagination = paginator.page(1)
    except EmptyPage:
        course_categories_pagination = paginator.page(paginator.num_pages)

    context = {
        "course_categories_list": course_categories_list,
        "course_categories_pagination": course_categories_pagination,
        "course_categories_limit": course_categories_limit,
        "course_sub_categories_list": course_sub_categories_list,
        "course_sub_to_sub_categories_list": course_sub_to_sub_categories_list,
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
        instance.course_category_creator = request.user
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_category_creator
        act.act_title = "Kurs Kategori Eklendi: " + form.cleaned_data.get("course_category_title")
        act.act_created_date = instance.course_category_created_date
        act.act_method = "POST"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_category_description")
        act.save()
        return redirect("admin_index")
    return render(request, "admin/course/add-category.html", context)


@login_required(login_url="login_admin")
def admin_edit_course_category(request, course_category_slug):
    instance = get_object_or_404(CourseCategory, course_category_slug=course_category_slug)
    form = CourseCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_category_creator
        act.act_title = "Kurs Kategori Düzenlendi: " + form.cleaned_data.get("course_category_title")
        act.act_created_date = instance.course_category_created_date
        act.act_method = "UPDATE"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_category_description")
        act.save()
        return redirect("admin_index")
    return render(request, "admin/course/edit-category.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_course_category(request, course_category_slug):
    instance = get_object_or_404(CourseCategory, course_category_slug=course_category_slug)
    instance.delete()
    return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_course_sub_category(request):
    keyword = request.GET.get("keyword")
    if keyword:
        course_sub_categories_pagination = CourseSubCategory.objects.filter(
            Q(id__contains=keyword) |
            Q(course_sub_category_title__contains=keyword) |
            Q(course_sub_category_created_date__contains=keyword) |
            Q(course_sub_category_slug__contains=keyword) | Q(course_category_id__contains=keyword))
        context = {
            "course_sub_categories_pagination": course_sub_categories_pagination,
        }
        return render(request, "admin/course/sub-categories.html", context)

    course_sub_categories_list = CourseSubCategory.objects.all()
    course_sub_categories_limit = CourseSubCategory.objects.all().order_by('-course_sub_category_created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(course_sub_categories_limit, 5)
    try:
        course_sub_categories_pagination = paginator.page(page)
    except PageNotAnInteger:
        course_sub_categories_pagination = paginator.page(1)
    except EmptyPage:
        course_sub_categories_pagination = paginator.page(paginator.num_pages)

    context = {
        "course_sub_categories_list": course_sub_categories_list,
        "course_sub_categories_pagination": course_sub_categories_pagination,
        "course_sub_categories_limit": course_sub_categories_limit,
    }
    return render(request, "admin/course/sub-categories.html", context)


@login_required(login_url="login_admin")
def admin_add_course_sub_category(request):
    form = CourseSubCategoryForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.course_sub_category_creator = request.user
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_sub_category_creator
        act.act_title = "Kurs Kategori Eklendi: " + form.cleaned_data.get("course_sub_category_title")
        act.act_created_date = instance.course_sub_category_created_date
        act.act_method = "POST"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_sub_category_description")
        act.save()
        return redirect("admin_index")
    return render(request, "admin/course/add-sub-category.html", context)


@login_required(login_url="login_admin")
def admin_edit_course_sub_category(request, course_sub_category_slug):
    instance = get_object_or_404(CourseSubCategory, course_sub_category_slug=course_sub_category_slug)
    form = CourseSubCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_sub_category_creator
        act.act_title = "Kurs Alt Kategori Düzenlendi: " + form.cleaned_data.get("course_sub_category_title")
        act.act_created_date = instance.course_sub_category_created_date
        act.act_method = "UPDATE"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_sub_category_description")
        act.save()
        return redirect("admin_index")
    return render(request, "admin/course/edit-sub-category.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_course_sub_category(request, course_sub_category_slug):
    instance = get_object_or_404(CourseSubCategory, course_sub_category_slug=course_sub_category_slug)
    instance.delete()
    return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_course_sub_to_sub_category(request):
    keyword = request.GET.get("keyword")
    if keyword:
        course_sub_to_sub_categories_pagination = CourseSubToSubCategory.objects.filter(
            Q(id__contains=keyword) |
            Q(course_sub_to_sub_category_title__contains=keyword) |
            Q(course_sub_to_sub_category_created_date__contains=keyword) |
            Q(course_sub_to_sub_category_slug__contains=keyword) | Q(course_sub_category_id__contains=keyword))
        context = {
            "course_sub_to_sub_categories_pagination": course_sub_to_sub_categories_pagination,
        }
        return render(request, "admin/course/sub-to-sub-categories.html", context)

    course_sub_to_sub_categories_list = CourseSubToSubCategory.objects.all()
    course_sub_to_sub_categories_limit = CourseSubToSubCategory.objects.all().order_by(
        '-course_sub_to_sub_category_created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(course_sub_to_sub_categories_limit, 5)
    try:
        course_sub_to_sub_categories_pagination = paginator.page(page)
    except PageNotAnInteger:
        course_sub_to_sub_categories_pagination = paginator.page(1)
    except EmptyPage:
        course_sub_to_sub_categories_pagination = paginator.page(paginator.num_pages)

    context = {
        "course_sub_to_sub_categories_list": course_sub_to_sub_categories_list,
        "course_sub_to_sub_categories_pagination": course_sub_to_sub_categories_pagination,
        "course_sub_to_sub_categories_limit": course_sub_to_sub_categories_limit,
    }
    return render(request, "admin/course/sub-to-sub-categories.html", context)


@login_required(login_url="login_admin")
def admin_add_course_sub_to_sub_category(request):
    form = CourseSubToSubCategoryForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.course_sub_to_sub_category_creator = request.user
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_sub_to_sub_category_creator
        act.act_title = "Kurs En Alt Kategori Eklendi: " + form.cleaned_data.get("course_sub_to_sub_category_title")
        act.act_created_date = instance.course_sub_to_sub_category_created_date
        act.act_method = "POST"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_sub_to_sub_category_description")
        act.save()
        return redirect("admin_index")
    return render(request, "admin/course/add-sub-to-sub-category.html", context)


@login_required(login_url="login_admin")
def admin_edit_course_sub_to_sub_category(request, course_sub_to_sub_category_slug):
    instance = get_object_or_404(CourseSubToSubCategory,
                                 course_sub_to_sub_category_slug=course_sub_to_sub_category_slug)
    form = CourseSubToSubCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        act = AdminActivity()
        act.act_creator = instance.course_sub_to_sub_category_creator
        act.act_title = "Kurs En Alt Kategori Düzenlendi: " + form.cleaned_data.get("course_sub_to_sub_category_title")
        act.act_created_date = instance.course_sub_to_sub_category_created_date
        act.act_method = "UPDATE"
        act.act_app = "Kurs"
        act.act_desc = "Açıklama: " + form.cleaned_data.get("course_sub_to_sub_category_description")
        act.save()
        return redirect("admin_index")
    return render(request, "admin/course/edit-sub-to-sub-category.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_course_sub_to_sub_category(request, course_sub_to_sub_category_slug):
    instance = get_object_or_404(CourseSubToSubCategory,
                                 course_sub_to_sub_category_slug=course_sub_to_sub_category_slug)
    instance.delete()
    return redirect("course_category")