import datetime
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect, render
from django.utils.functional import SimpleLazyObject
from django.views.generic import RedirectView, FormView
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse_lazy

from account.forms import AccountUpdatePasswordForm
from account.models import Account, Group, AccountGroup, AccountSocialMedia, AccountPermission, \
    AccountActivity, SocialMedia
from article.models import Article, ArticleComment
from question.models import Question


def index(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "ankades/dashboard.html", context)


@login_required(login_url="login_account")
def account_detail(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, username)
    try:
        userDetail = Account.objects.get(username=username)
        accountActivity = AccountActivity.objects.filter(creator=userDetail).values('createdDate').order_by('createdDate')
        context = {
            "userDetail": userDetail,
            "userGroup": userGroup,
            "currentUser": currentUser,
            "accountActivity": accountActivity,
        }
        return render(request, "ankades/account/account-detail.html", context)
    except:
        messages.error(request, "Kullanıcı bulunamadı")
        return redirect("index")


def login_account(request):
    """
    :param request:
    :return:
    """
    activity = AccountActivity()
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            remember = request.POST.get("remember")
            try:
                get_user = Account.objects.get(username=username)
                if not get_user.is_active:
                    messages.error(request, "Kullanıcı engelli olduğu için giriş yapılamadı.")
                    return redirect("login_account")
            except Account.DoesNotExist:
                messages.error(request, "Böyle bir kullanıcı bulunamadı.")
                return redirect("login_account")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                messages.error(request, "Şifre hatalı.")
                return redirect("login_admin")
            login(request, user)
            if remember:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            activity.creator = user
            activity.method = "POST"
            activity.title = "Kullanıcı giriş yaptı"
            activity.createdDate = datetime.datetime.now()
            activity.application = "Account"
            activity.description = "" + str(activity.creator.username) + " giriş yaptı."
            activity.save()
            messages.success(request, "Başarıyla giriş yapıldı.")
            return redirect("index")
        return render(request, "ankades/registration/login.html")
    else:
        messages.warning(request, "Zaten giriş yapılmış.")
        return redirect("index")


@login_required(login_url="login_account")
def logout_account(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    if request.user.is_authenticated:
        logout(request)
        activity.title = "Çıkış Yapma."
        activity.application = "Logout"
        activity.method = "UPDATE"
        activity.createdDate = datetime.datetime.now()
        activity.creator = currentUser
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı çıkış yaptı."
        activity.save()
        messages.success(request, "Başarıyla çıkış yapıldı")
        return redirect("index")
    else:
        return redirect("index")


def register_account(request):
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        activity = AccountActivity()
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password and confirm_password and password != confirm_password:
                messages.error(request, "Şifreler uyuşmuyor. Lütfen tekrar deneyin.")
                return render(request, "ankades/registration/register.html")
            elif Account.objects.filter(email=email):
                messages.error(request, "Bu email adresinde kullanıcı mevcut")
                return render(request, "ankades/registration/register.html")
            elif Account.objects.filter(username=username):
                messages.error(request, "Bu kullanıcı adı sistemimizde mevcut")
                return render(request, "ankades/registration/register.html")
            else:
                new_user = Account(first_name=first_name, last_name=last_name, username=username, email=email)
                new_user.is_active = True
                new_user.save()
                new_user.set_password(password)
                new_user.save()
                getGroup = Group.objects.get(slug="uye")
                new_group = AccountGroup(userId=new_user, groupId=getGroup)
                new_group.save()
                new_user = authenticate(username=username, password=password)
                login(request, new_user)
                activity.title = "Kayıt Olma"
                activity.application = "ACCOUNT"
                activity.method = "POST"
                activity.creator = new_user
                activity.createdDate = datetime.datetime.now()
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kayıt oldu."
                activity.save()
            messages.success(request, "Kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("login_account")
        return render(request, "ankades/registration/register.html")
    else:
        messages.error(request, "Zaten giriş yapılmış.")
        return redirect("index")


def get_requested_user(request, username):
    currentUser = request.user
    userGroup = current_user_group(request, username)
    userDetail = get_object_or_404(Account, username=username)
    context = {
        "userDetail": userDetail,
        "userGroup": userGroup,
        "currentUser": currentUser,
    }
    return render(request, "ankades/account/account-profile.html", context)


class FollowAccountToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs.get("username")
        obj = get_object_or_404(Account, username=username)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.follower.all():
                obj.follower.remove(user)
            else:
                obj.follower.add(user)
        return url_


def current_user_group(self, username):
    try:
        group = AccountGroup.objects.get(userId__username=username)
        return str(group.groupId)
    except:
        group = None
        return group


def current_user_permission(self, username):
    try:
        userPermission = AccountPermission.objects.get(userId__username=username)
        return str(userPermission.permissionId)
    except:
        userPermission = None
        return userPermission


def user_social_media(self, username):
    try:
        usm = AccountSocialMedia.objects.get(userId__username=username)
        return str(usm)
    except:
        usm = None
        return usm


def user_articles(self, username):
    try:
        articles = Article.objects.filter(creator__username=username)
        return articles
    except:
        articles = None
        return articles


def user_questions(self, username):
    try:
        questions = Question.objects.filter(creator__username=username)
        return questions
    except:
        questions = None
        return questions


def get_social_media(self, slug):
    try:
        socialMedia = get_object_or_404(SocialMedia, slug=slug)
        return socialMedia.id
    except:
        socialMedia = None
        return socialMedia


# def get_user_timeline(request, username):
#     currentUser = request.user
#     userGroup = current_user_group(request, currentUser)
#     try:
#         accountActivity = AccountActivity.objects.get(creator__username=username)
#         context = {
#             "currentUser": currentUser,
#             "userGroup": userGroup,
#             "accountActivity": accountActivity,
#         }
#         return render(request, "ankades/account/timeline.html", context)
#     except:
#         messages.error(request, "Kullanıcı bulunamadı.")
#         return render(request, "404.html")