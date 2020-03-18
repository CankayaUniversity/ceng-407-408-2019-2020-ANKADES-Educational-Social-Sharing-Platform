import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect
from online_users.models import OnlineUserActivity
from rest_framework.generics import get_object_or_404
from account.models import Account, Permission, SocialMedia, AccountGroup
from account.views.views import current_user_group
from adminpanel.forms import AdminLoginForm, AdminSocialMediaForm, AdminEditSocialMediaForm, AdminTagForm
from adminpanel.models import Tag, AdminActivity
from article.models import ArticleCategory, Article
from course.models import CourseCategory, Course
from exam.models import Exam, School


@login_required(login_url="login_account")
def admin_dashboard(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    user_activity_objects = OnlineUserActivity.get_user_activities(datetime.timedelta(minutes=2))
    number_of_active_users = user_activity_objects.count()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "user_activity_objects": user_activity_objects,
        "number_of_active_users": number_of_active_users,
    }
    if userGroup == 'admin':
        return render(request, "adminpanel/dashboard.html", context)
    else:
        return redirect("index")


def login_admin(request):
    if request.user.is_authenticated:
        return redirect("logout_account")
    else:
        isAdmin = True
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
                        return redirect("admin_dashboard")
                    else:
                        messages.error(request, "Kullanıcı aktif değil !")
                        return redirect("admin_dashboard")
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
    return None
    # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    # context = {
    #     "adminGroup": adminGroup,
    # }
    # return render(request, "admin/settings/site-settings.html", context)


# Account Settings
@login_required(login_url="login_admin")
def admin_account_settings(request):
    # accounts = Account.objects.all()
    # accountGroups = AccountGroup.objects.all()
    # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    # accountFiveLimitOrdered = Account.objects.all().order_by('-date_joined')[:5]
    # context = {
    #     "accounts": accounts,
    #     "accountGroups": accountGroups,
    #     "accountFiveLimitOrdered": accountFiveLimitOrdered,
    #     "adminGroup": adminGroup,
    # }
    # if adminGroup:
    #     return render(request, "admin/settings/account-settings.html", context)
    # else:
    #     messages.error(request, "Yetkiniz yok")
    #     return redirect("admin_dashboard")
    return None


# Social Media Settings
@login_required(login_url="login_admin")
def admin_all_social_medias(request):
    socialMedias = SocialMedia.objects.all()
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "socialMedias": socialMedias,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/social-medias.html", context)


@login_required(login_url="login_admin")
def admin_add_social_media(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    if request.method == "POST" and request.FILES['media']:
        title = request.POST.get("title")
        isActive = request.POST.get("isActive") == 'on'
        media = request.FILES['media']
        fs = FileSystemStorage()
        fs.save(media.name, media)
        if SocialMedia.objects.filter(title=title):
            messages.error(request, "Bu sosyal medya daha önce eklenmiş")
            return redirect("admin_add_social_media")
        else:
            new_sm = SocialMedia(title=title, media=media, isActive=isActive)
            new_sm.save()
            messages.success(request, "Sosyal Medya kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("admin_all_social_medias")
    context = {
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/add-social-media.html", context)


@login_required(login_url="login_admin")
def admin_edit_social_media(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    # instance = get_object_or_404(SocialMedia, slug=slug)
    # form = AdminEditSocialMediaForm(request.POST or None, instance=instance)
    # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    # context = {
    #     "form": form,
    #     "adminGroup": adminGroup,
    # }
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.title = form.cleaned_data.get("title")
    #     instance.slug = form.cleaned_data.get("slug")
    #     instance.updatedDate = datetime.datetime.now()
    #     instance.save()
    #     messages.success(request, "Sosyal medya başarıyla düzenlendi !")
    #     return redirect("admin_social_media_settings")
    # return render(request, "admin/settings/edit-social-media.html", context)
    return None


# Group Settings
@login_required(login_url="login_admin")
def admin_group_settings(request):
    # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    # context = {
    #     "adminGroup": adminGroup,
    # }
    # return render(request, "admin/settings/group-settings.html", context)
    return None


# Permission Settings
@login_required(login_url="login_admin")
def admin_permission_settings(request):
    # permissions = Permission.objects.all()
    # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    # context = {
    #     "permissions": permissions,
    #     "adminGroup": adminGroup,
    # }
    # return render(request, "admin/settings/permission-settings.html", context)
    return None


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
        "form": form,
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