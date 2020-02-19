from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from account.models import Account, MainGroup, MainPermission
from adminpanel.forms import AdminLoginForm, CourseCategoryForm, CourseSubCategoryForm, CourseSubToSubCategoryForm, \
    AdminEditProfileForm, CourseForm, AddAccountMainPermissionForm, AddAccountMainGroupForm, \
    AddAccountGroupPermissionForm, AddAccountGroupForm, AddAccountHasPermission
from adminpanel.models import AdminActivity
from adminpanel.serializers import AccountPermissionsSerializer, AccountGroupsSerializer, AdminActivitySerializer
from course.models import CourseCategory, CourseSubCategory, Course, CourseSubToSubCategory


# UserViewSet
class AccountGroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = AccountGroupsSerializer


class AccountPermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = AccountPermissionsSerializer


class AdminActivityViewSet(viewsets.ModelViewSet):
    queryset = AdminActivity.objects.all()
    serializer_class = AdminActivitySerializer


# Dashboard View
@login_required(login_url="login_admin")
def admin_index(request):
    if request.user.is_superuser:
        user = Account.objects.all()
        user_count = Account.objects.all().count()
        course_count = Course.objects.all().count()
        course_category_count = CourseCategory.objects.all().count()
        course_sub_category_count = CourseSubCategory.objects.all().count()
        course_sub_to_sub_category_count = CourseSubToSubCategory.objects.all().count()
        activity = AdminActivity.objects.all()
        activity_limit = AdminActivity.objects.all().order_by("-act_created_date")[:4]
        context = {
            "user": user,
            "user_count": user_count,
            "course_count": course_count,
            "course_category_count": course_category_count,
            "course_sub_category_count": course_sub_category_count,
            "course_sub_to_sub_category_count": course_sub_to_sub_category_count,
            "activity": activity,
            "activity_limit": activity_limit,
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
        return render(request, "admin/account/all-users.html", context)

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
    return render(request, "admin/account/all-users.html", context)


@login_required(login_url="login_admin")
def admin_edit_profile(request, username):
    instance = get_object_or_404(Account, username=username)
    form = AdminEditProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.username = username
        instance.save()
        context = {
            "form": form,
        }
        return render(request, "admin/account/edit-profile.html", context)
    return render(request, "admin/account/edit-profile.html", {"form": form})


@login_required(login_url="login_admin")
def admin_get_groups(request):
    return None
#End Of User View


#Course View
@login_required(login_url="login_admin")
def courses(request):
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
def add_course(request):
    form = CourseForm(request.POST or None)
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
    context = {
        "form": form,
    }
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
#End Of Course View

#Course Category View
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
def add_course_category(request):
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

#End Of Course Category View

#Course Sub Category View
@login_required(login_url="login_admin")
def course_sub_category(request):
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
def add_course_sub_category(request):
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


#Course Sub To Sub Category View
@login_required(login_url="login_admin")
def course_sub_to_sub_category(request):
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
    course_sub_to_sub_categories_limit = CourseSubToSubCategory.objects.all().order_by('-course_sub_to_sub_category_created_date')[:5]
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
def add_course_sub_to_sub_category(request):
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


def admin_edit_course_sub_to_sub_category(request, course_sub_to_sub_category_slug):
    instance = get_object_or_404(CourseSubToSubCategory, course_sub_to_sub_category_slug=course_sub_to_sub_category_slug)
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


#add group
@login_required(login_url="login_admin")
def add_account_main_group(request):
    form = AddAccountMainGroupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/groups/add-group.html", context)


@login_required(login_url="login_admin")
def add_account_main_permission(request):
    form = AddAccountMainPermissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-permission.html", context)


@login_required(login_url="login_admin")
def add_account_group_permission(request):
    form = AddAccountGroupPermissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-group-perm.html", context)


@login_required(login_url="login_admin")
def add_account_group(request):
    form = AddAccountGroupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-account-group.html", context)


@login_required(login_url="login_admin")
def add_account_has_permission(request):
    form = AddAccountHasPermission(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-account-has-per.html", context)


@login_required(login_url="login_admin")
def all_groups(request):
    groups = MainGroup.objects.all()
    context = {
        "groups": groups,
    }
    return render(request, "admin/groups/groups.html", context)


@login_required(login_url="login_admin")
def all_permissions(request):
    permissions = MainPermission.objects.all()
    context = {
        "permissions": permissions,
    }
    return render(request, "admin/permissions/all-permissions.html", context)


@login_required(login_url="login_admin")
def delete_main_permission(request, name_slug):
    instance = get_object_or_404(MainPermission, name_slug=name_slug)
    instance.delete()
    return redirect("all_permissions")


@login_required(login_url="login_admin")
def edit_main_permission(request, name_slug):
    instance = get_object_or_404(MainPermission, name_slug=name_slug)
    form = AddAccountMainPermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("all_permissions")
    return render(request, "admin/permissions/edit-main-permission.html", {"form": form})


@login_required(login_url="login_admin")
def delete_main_group(request, name_slug):
    instance = get_object_or_404(MainGroup, name_slug=name_slug)
    instance.delete()
    return redirect("all_groups")


@login_required(login_url="login_admin")
def edit_main_group(request, name_slug):
    instance = get_object_or_404(MainGroup, name_slug=name_slug)
    form = AddAccountMainGroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("all_groups")
    return render(request, "admin/groups/edit-main-group.html", {"form": form})