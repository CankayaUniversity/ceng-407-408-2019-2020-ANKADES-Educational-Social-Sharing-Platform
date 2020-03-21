import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from online_users.models import OnlineUserActivity
from account.models import Account, AccountGroup
from account.views.views import current_user_group
from adminpanel.forms import AdminLoginForm, AdminTagForm
from adminpanel.models import Tag
from article.models import Article
from course.models import Course


@login_required(login_url="login_account")
def admin_dashboard(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    user_activity_objects = OnlineUserActivity.get_user_activities(datetime.timedelta(minutes=2))
    number_of_active_users = user_activity_objects.count()
    userCount = Account.objects.all().count()
    articleCount = Article.objects.all().count()
    courseCount = Course.objects.all().count()
    sum = articleCount + courseCount
    context = {
        "userGroup": userGroup,
        "userCount": userCount,
        "articleCount": articleCount,
        "courseCount": courseCount,
        "sum": sum,
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
    return render(request, "adminpanel/tags/add-tag.html", context)