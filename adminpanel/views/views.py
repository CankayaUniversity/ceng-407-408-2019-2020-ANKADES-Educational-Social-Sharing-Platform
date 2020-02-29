from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account, AccountGroup, Permission
from adminpanel.forms import AdminLoginForm
from adminpanel.models import AdminActivity
from course.models import CourseCategory, Course


# Dashboard View
@login_required(login_url="login_admin")
def admin_index(request):
    if request.user.is_superuser:
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
            # "activity": activity,
            # "activity_limit": activity_limit,
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
                    messages.success(request, "Hoş geldiniz " + user.get_full_name())
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


#Site Settings
@login_required(login_url="login_admin")
def admin_settings(request):
    return render(request, "admin/settings/site-settings.html")


#Account Settings
@login_required(login_url="login_admin")
def admin_account_settings(request):
    accounts = Account.objects.all()
    accountGroups = AccountGroup.objects.all()
    accountFiveLimitOrdered = Account.objects.all().order_by('-date_joined')[:5]
    context = {
        "accounts": accounts,
        "accountGroups": accountGroups,
        "accountFiveLimitOrdered": accountFiveLimitOrdered,
    }
    return render(request, "admin/settings/account-settings.html", context)


#Social Media Settings
@login_required(login_url="login_admin")
def admin_social_media_settings(request):
    return render(request, "admin/settings/social-media-settings.html")


#Group Settings
@login_required(login_url="login_admin")
def admin_group_settings(request):
    return render(request, "admin/settings/group-settings.html")


#Permission Settings
@login_required(login_url="login_admin")
def admin_permission_settings(request):
    permissions = Permission.objects.all()
    context = {
        "permissions": permissions
    }
    return render(request, "admin/settings/permission-settings.html", context)

