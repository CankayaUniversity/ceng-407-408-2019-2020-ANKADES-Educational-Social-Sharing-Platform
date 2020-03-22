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


@login_required(login_url="login_admin")
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
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            remember = request.POST.get("remember")
            user = authenticate(username=username, password=password)
            try:
                get_user = Account.objects.get(username=username)
                if not get_user.is_staff:
                    messages.error(request, "Admin panele giriş yetkiniz yok.")
                    return redirect("admin_dashboard")
            except Account.DoesNotExist:
                return redirect("admin_dashboard")

            login(request, user)
            if remember:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            messages.success(request, "Başarıyla giriş yapıldı.")
            return redirect("admin_dashboard")
        return render(request, "adminpanel/registration/login.html")
    else:
        messages.warning(request, "Zaten giriş yapılmış.")
        return redirect("admin_dashboard")


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
    return render(request, "adminpanel/tags/all-tags.html", context)


@login_required(login_url="login_admin")
def admin_add_tag(request):
    """
    :param request:
    :return:
    """
    return None


@login_required(login_url="login_admin")
def admin_edit_tag(request):
    """
    :param request:
    :return:
    """
    return None


@login_required(login_url="login_admin")
def admin_isactive_tag(request):
    """
    :param request:
    :return:
    """
    return None


@login_required(login_url="login_admin")
def admin_delete_tag(request):
    """
    :param request:
    :return:
    """
    return None