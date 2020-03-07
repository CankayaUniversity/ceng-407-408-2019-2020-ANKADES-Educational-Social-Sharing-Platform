import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import Account, AccountGroup, Permission, SocialMedia
from adminpanel.forms import AdminLoginForm, AdminSocialMediaForm, AdminEditSocialMediaForm, AdminTagForm
from adminpanel.models import Tag
from course.models import CourseCategory, Course


# Dashboard View
@login_required(login_url="login_admin")
def admin_index(request):
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    # if AccountGroup.objects.filter(
    #         Q(userId__username=request.user.username, groupId__slug="moderator") | Q(
    #             userId__username=request.user.username, groupId__slug="admin")):
    if adminGroup:
        user = Account.objects.all()
        admin = AccountGroup.objects.filter(groupId__slug__contains="admin")
        moderator = AccountGroup.objects.filter(groupId__slug__contains="moderator")
        ogretmen = AccountGroup.objects.filter(groupId__slug__contains="ogretmen")
        ogrenci = AccountGroup.objects.filter(groupId__slug__contains="ogrenci")
        user_count = Account.objects.all().count()
        course_count = Course.objects.all().count()
        course_category_count = CourseCategory.objects.all().count()
        # activity = AdminActivity.objects.all()
        # activity_limit = AdminActivity.objects.all().order_by("-activityCreatedDate")[:4]
        context = {
            "user": user,
            "ogrenci": ogrenci,
            "moderator": moderator,
            "ogretmen": ogretmen,
            "admin": admin,
            "user_count": user_count,
            "course_count": course_count,
            "course_category_count": course_category_count,
            "adminGroup": adminGroup,
            # "activity": activity,
            # "activity_limit": activity_limit,
        }
        return render(request, "admin/index.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("index")
    return render(request, "admin/index.html", context)


# User View
def login_admin(request):
    if request.user.is_authenticated:
        messages.error(request, "Zaten Giriş Yapılmış")
        return redirect("admin_index")
    else:
        form = AdminLoginForm(request.POST or None)
        context = {"form": form}
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            accountGroup = AccountGroup.objects.filter(
                Q(userId__username=form.cleaned_data.get('username'), groupId__slug="moderator") | Q(
                    userId__username=form.cleaned_data.get('username'), groupId__slug="admin"))
            if accountGroup:
                user = authenticate(username=username, password=password)
                if user is None:
                    return render(request, "admin/login.html", {"form": form, "accountGroup": accountGroup})
                else:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "Hoş geldiniz " + user.get_full_name())
                        return redirect("admin_index")
                    else:
                        messages.error(request, "Kullanıcı aktif değil !")
                        return redirect("admin_index")
            else:
                messages.error(request,
                               "Admin paneline giriş yetkiniz yok ya da böyle bir kullanıcı bulunamadı! Log alındı.")
                return redirect("login_admin")
    return render(request, "admin/login.html", context)


@login_required(login_url="login_admin")
def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login_admin")
    else:
        return redirect("login_admin")


# Site Settings
@login_required(login_url="login_admin")
def admin_settings(request):
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "adminGroup": adminGroup,
    }
    return render(request, "admin/settings/site-settings.html", context)


# Account Settings
@login_required(login_url="login_admin")
def admin_account_settings(request):
    accounts = Account.objects.all()
    accountGroups = AccountGroup.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    accountFiveLimitOrdered = Account.objects.all().order_by('-date_joined')[:5]
    context = {
        "accounts": accounts,
        "accountGroups": accountGroups,
        "accountFiveLimitOrdered": accountFiveLimitOrdered,
        "adminGroup": adminGroup
    }
    return render(request, "admin/settings/account-settings.html", context)


# Social Media Settings
@login_required(login_url="login_admin")
def admin_social_media_settings(request):
    socialMedias = SocialMedia.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "socialMedias": socialMedias,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/settings/social-media-settings.html", context)


@login_required(login_url="login_admin")
def admin_add_social_media(request):
    form = AdminSocialMediaForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
            title = form.cleaned_data.get("title")
            slug = form.cleaned_data.get("slug")
            isActive = form.cleaned_data.get("isActive")
            if SocialMedia.objects.filter(title=title) or SocialMedia.objects.filter(
                    slug=slug):
                messages.error(request, "Bu sosyal medya daha önce eklenmiş")
                return redirect("admin_add_social_media")
            else:
                new_sm = SocialMedia(title=title, slug=slug, isActive=isActive)
                new_sm.save()
                messages.success(request, "Sosyal Medya kayıt işlemi başarıyla gerçekleştirildi.")
                return redirect("admin_social_media_settings")
        context = {
            "form": form,
            "adminGroup": adminGroup
        }
        return render(request, "admin/settings/add-social-media.html", context)
    else:
        messages.error(request, "Yetkiniz Yok !")


@login_required(login_url="login_admin")
def admin_edit_social_media(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(SocialMedia, slug=slug)
    form = AdminEditSocialMediaForm(request.POST or None, instance=instance)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "form": form,
        "adminGroup": adminGroup,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.title = form.cleaned_data.get("title")
        instance.slug = form.cleaned_data.get("slug")
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Sosyal medya başarıyla düzenlendi !")
        return redirect("admin_social_media_settings")
    return render(request, "admin/settings/edit-social-media.html", context)


# Group Settings
@login_required(login_url="login_admin")
def admin_group_settings(request):
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "adminGroup": adminGroup,
    }
    return render(request, "admin/settings/group-settings.html", context)


# Permission Settings
@login_required(login_url="login_admin")
def admin_permission_settings(request):
    permissions = Permission.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "permissions": permissions,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/settings/permission-settings.html", context)


@login_required(login_url="login_admin")
def admin_tags(request):
    """
    :param request:
    :return:
    """
    tags = Tag.objects.all()
    context = {
        "tags": tags,
    }
    return render(request, "admin/tags/all-tags.html", context)


@login_required(login_url="login_admin")
def admin_add_tag(request):
    """
    :param request:
    :return:
    """
    form = AdminTagForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        title = form.cleaned_data.get("title")
        isActive = form.cleaned_data.get("isActive")
        instance = Tag(title=title, isActive=isActive)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Etiket başarıyla eklendi !")
        return redirect("admin_tags")
    return render(request, "admin/tags/add-tag.html", context)