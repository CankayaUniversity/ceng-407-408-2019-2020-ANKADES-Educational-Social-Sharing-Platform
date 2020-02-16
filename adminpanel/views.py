from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from account.models import Account
from adminpanel.forms import AdminLoginForm, CourseCategoryForm, CourseSubCategoryForm, CourseSubToSubCategoryForm, \
    AdminEditProfileForm
from adminpanel.models import Activity
from adminpanel.serializers import AccountPermissionsSerializer, AccountGroupsSerializer
from course.models import CourseCategory, CourseSubCategory, Course, CourseSubToSubCategory


# UserViewSet
class AccountGroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = AccountGroupsSerializer


class AccountPermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = AccountPermissionsSerializer


# Main View
@login_required(login_url="login_admin")
def admin_index(request):
    if request.user.is_superuser:
        user = Account.objects.all()
        user_count = Account.objects.all().count()
        course_count = Course.objects.all().count()
        course_category_count = CourseCategory.objects.all().count()
        course_sub_category_count = CourseSubCategory.objects.all().count()
        course_sub_to_sub_category_count = CourseSubToSubCategory.objects.all().count()
        activity = Activity.objects.all()
        context = {
            "user": user,
            "user_count": user_count,
            "course_count": course_count,
            "course_category_count": course_category_count,
            "course_sub_category_count": course_sub_category_count,
            "course_sub_to_sub_category_count": course_sub_to_sub_category_count,
            "activity": activity,
        }
        return render(request, "admin/index.html", context)
    else:
        return redirect("admin_index")


# User View
def login_admin(request):
    if not request.user.is_authenticated:
        form = AdminLoginForm(request.POST or None)
        context = {
            "form": form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is None:
                return render(request, "admin/login.html", context)
            else:
                if user.is_active and user.is_superuser:
                    login(request, user)
                    return redirect("admin_index")
                else:
                    return render(request, "admin/login.html", context)
        else:
            return render(request, "admin/login.html", context)
    else:
        return redirect("admin_index")


@login_required(login_url="login_admin")
def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login_admin")
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def users_table(request):
    keyword = request.GET.get("keyword")
    if keyword:
        user_pagination = Account.objects.filter(
            Q(username__contains=keyword) |
            Q(first_name__contains=keyword) |
            Q(id__contains=keyword) |
            Q(last_name__contains=keyword))
        context = {
            "user_pagination": user_pagination,
        }
        return render(request, "admin/account/all_users.html", context)

    users_list = Account.objects.all()
    users_limit = Account.objects.all().order_by('-date_joined')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(users_limit, 5)
    try:
        user_pagination = paginator.page(page)
    except PageNotAnInteger:
        user_pagination = paginator.page(1)
    except EmptyPage:
        user_pagination = paginator.page(paginator.num_pages)

    context = {
        "users_list": users_list,
        "user_pagination": user_pagination,
        "users_limit": users_limit,
    }
    return render(request, "admin/account/all_users.html", context)


@login_required(login_url="login_admin")
def add_course_category(request):
    form = CourseCategoryForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        course = form.save(commit=False)
        course.course_category_creator = request.user
        course.save()
        activity_save = Activity()
        activity_save.creator = course.course_category_creator
        activity_save.activity = "Kurs Kategori Eklendi: " + form.cleaned_data.get("course_category_title")
        activity_save.activity_created_date = course.course_category_created_date
        activity_save.activity_action = "Post"
        activity_save.activity_application = "Kurs"
        activity_save.activity_description = "Açıklama: " + form.cleaned_data.get("course_category_description")
        activity_save.save()
        return redirect("admin_index")
    return render(request, "admin/course/add-category.html", context)


@login_required(login_url="login_admin")
def edit_course_category(request, course_category_slug):
    instance = get_object_or_404(CourseCategory, course_category_slug=course_category_slug)
    form = CourseCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    return render(request, "admin/course/edit-category.html", {"form": form})


@login_required(login_url="login_admin")
def delete_course_category(request, course_category_slug):
    course_category = get_object_or_404(CourseCategory, course_category_slug=course_category_slug)
    course_category.delete()
    return redirect("admin_index")


@login_required(login_url="login_admin")
def delete_course_sub_category(request, course_sub_category_slug):
    course_sub_category = get_object_or_404(CourseSubCategory, course_sub_category_slug=course_sub_category_slug)
    course_sub_category.delete()
    return redirect("admin_index")


@login_required(login_url="login_admin")
def edit_course_sub_category(request, course_sub_category_slug):
    instance = get_object_or_404(CourseSubCategory, course_sub_category_slug=course_sub_category_slug)
    form = CourseSubCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    return render(request, "admin/course/edit-sub-category.html", {"form": form})


@login_required(login_url="adminpanel:login_admin")
def sub_categories(request):
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
def course_category(request):
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
        return render(request, "admin/course/categories.html", context)

    course_categories_list = CourseCategory.objects.all()
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
        "course_sub_categories_pagination": course_categories_pagination,
        "course_categories_limit": course_categories_limit,
    }
    return render(request, "admin/course/categories.html", context)


@login_required(login_url="login_admin")
def add_course_sub_category(request):
    form = CourseSubCategoryForm(request.POST or None)
    if form.is_valid():
        add_course_sub_category = form.save(commit=False)
        add_course_sub_category.save()
        return redirect("admin_index")
    return render(request, "admin/course/add-sub-category.html", {"form": form})


@login_required(login_url="login_admin")
def add_course_sub_to_subcategory(request):
    form = CourseSubToSubCategoryForm(request.POST or None)
    if form.is_valid():
        add_course_sub_to_sub_category = form.save(commit=False)
        add_course_sub_to_sub_category.save()
        return redirect("admin_index")
    return render(request, "admin/course/add-sub-to-sub-category.html", {"form": form})


@login_required(login_url="login_admin")
def add_course(request):
    return None


@login_required(login_url="adminpanel:login_admin")
def users_table(request):
    keyword = request.GET.get("keyword")
    if keyword:
        user_pagination = Account.objects.filter(
            Q(username__contains=keyword) |
            Q(first_name__contains=keyword) |
            Q(id__contains=keyword) |
            Q(last_name__contains=keyword))
        context = {
            "user_pagination": user_pagination,
        }
        return render(request, "admin/account/all_users.html", context)

    users_list = Account.objects.all()
    users_limit = Account.objects.all().order_by('-date_joined')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(users_limit, 5)
    try:
        user_pagination = paginator.page(page)
    except PageNotAnInteger:
        user_pagination = paginator.page(1)
    except EmptyPage:
        user_pagination = paginator.page(paginator.num_pages)

    context = {
        "users_list": users_list,
        "user_pagination": user_pagination,
        "users_limit": users_limit,
    }
    return render(request, "admin/account/all_users.html", context)

@login_required(login_url="login_admin")
def admin_edit_profile(request, username):
    if request.user.is_authenticated:
        instance = get_object_or_404(Account, username=username)
        users_list = Account.objects.all()
        get_user = Account.objects.get(username=username)
        form = AdminEditProfileForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            user = form.save(commit=False)
            user = user.username
            user.save()
            context = {
                "form": form,
                "get_user": get_user,
                "users_list": users_list,
            }
            return render(request, "admin/account/edit-profile.html", context)
        return render(request, "admin/account/edit-profile.html", {"form": form})
    else:
        return redirect("login_admin")
