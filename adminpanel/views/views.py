import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from online_users.models import OnlineUserActivity

from account.models import Account
from ankadescankaya.views import current_user_group
from adminpanel.models import Tag
from article.models import Article
from course.models import Course
from question.models import Question


@login_required(login_url="login_admin")
def admin_dashboard(request):
    """
    :param request: 
    :return: 
    """
    userGroup = current_user_group(request, request.user)
    user_activity_objects = OnlineUserActivity.get_user_activities(datetime.timedelta(minutes=2))
    number_of_active_users = user_activity_objects.count()
    userCount = Account.objects.all().count()
    articleCount = Article.objects.all().count()
    questionCount = Question.objects.all().count()
    courseCount = Course.objects.all().count()
    sum = articleCount + courseCount + questionCount
    context = {
        "userGroup": userGroup,
        "userCount": userCount,
        "articleCount": articleCount,
        "courseCount": courseCount,
        "sum": sum,
        "user_activity_objects": user_activity_objects,
        "number_of_active_users": number_of_active_users,
    }
    if userGroup == 'admin' or userGroup == 'moderator':
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
            try:
                get_user = Account.objects.get(username=username)
                if get_user.is_staff is not True or get_user.is_admin is not True:
                    messages.error(request, "Admin panele giriş yetkiniz yok.")
                    return redirect("index")
            except Account.DoesNotExist:
                messages.error(request, "Böyle bir kullanıcı bulunamadı.")
                return redirect("login_admin")
            user = authenticate(username=get_user, password=password)
            if user:
                login(request, user)
            else:
                messages.error(request, "Şifre hatalı.")
                return redirect("login_admin")
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
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yapıldı")
        return redirect("login_admin")
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_tags(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    tags = Tag.objects.all()
    context = {
        "tags": tags,
        "userGroup": userGroup,
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
