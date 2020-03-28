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
from account.models import Account, Group, AccountGroup, GroupPermission, AccountSocialMedia, AccountPermission, \
    AccountActivity, SocialMedia
from article.models import Article, ArticleComment


def index(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = 'Kullanıcı'
    if request.user.is_authenticated:
        userGroup = current_user_group(request, currentUser)
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup
    }
    return render(request, "ankades/dashboard.html", context)


@login_required(login_url="login_account")
def account_detail(request, username):
    userDetail = get_object_or_404(Account, username=username)
    if request.user.is_authenticated:
        currentUser = request.user
        userGroup = current_user_group(request, username)
        context = {
            "userDetail": userDetail,
            "userGroup": userGroup,
            "currentUser": currentUser,
        }
    else:
        context = {
            "userDetail": userDetail,
        }
    return render(request, "ankades/account/account-detail.html", context)


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
            user = authenticate(username=username, password=password)
            try:
                get_user = Account.objects.get(username=username)
                if not get_user.is_active:
                    messages.error(request, "Kullanıcı engelli olduğu için giriş yapılamadı.")
                    return redirect("login_account")
            except Account.DoesNotExist:
                return redirect("login_account")
            login(request, user)
            if remember:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            activity.creator = user
            activity.method = "POST"
            activity.title = "Kullanıcı giriş yaptı"
            activity.createdDate = datetime.datetime.now()
            activity.application = "ACCOUNT"
            activity.description = str(activity.creator.username) + " giriş yaptı."
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
        activity.application = "LOGOUT"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
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
        currentUser = request.user
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
                activity.title = "Giriş Yapma"
                activity.application = "REGISTER"
                activity.method = "UPDATE"
                activity.creator = currentUser
                activity.description = str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı giriş yaptı."
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
    group = AccountGroup.objects.get(userId__username=username)
    return str(group.groupId)


def user_group(self, username):
    group = AccountGroup.objects.get(userId__username=username)
    return group.groupId


def current_user_permission(self, username):
    userPermission = AccountPermission.objects.get(userId__username=username)
    return str(userPermission.permissionId)


def user_social_media(self, username):
    usm = AccountSocialMedia.objects.get(userId__username=username)
    return str(usm)


def user_articles(self, username):
    articles = Article.objects.filter(creator__username=username)
    return articles


def article_comment_count(self, slug):
    articleCommentCount = ArticleComment.objects.filter(articleId__slug=slug)
    return articleCommentCount


def get_social_media(self, slug):
    socialMedia = get_object_or_404(SocialMedia, slug=slug)
    return socialMedia.id
