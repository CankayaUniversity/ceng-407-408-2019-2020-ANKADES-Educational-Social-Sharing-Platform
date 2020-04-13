import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import RedirectView
from rest_framework.generics import get_object_or_404

from account.forms import SignUpForm
from account.models import Account, Group, AccountGroup, AccountSocialMedia, AccountPermission, \
    AccountLogs, SocialMedia, AccountFollower
from article.models import Article, ArticleCategory
from question.models import Question, QuestionCategory


def index(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articleCategories = ArticleCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
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
    userGroup = current_user_group(request, currentUser)
    try:
        userDetail = Account.objects.get(username=username)
        userDetailGroup = user_group(request, username)
        existFollower = get_user_follower(request, currentUser, userDetail)
        followers = AccountFollower.objects.filter(followingId__username=userDetail.username)
        followings = AccountFollower.objects.filter(followerId__username=userDetail.username)
        articles = user_articles(request, username)
        questions = user_questions(request, username)
        articleCategories = ArticleCategory.objects.filter(
            Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
        articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
        articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
        questionCategories = QuestionCategory.objects.filter(
            Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
        questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
        questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
        context = {
            "userDetail": userDetail,
            "userDetailGroup": userDetailGroup,
            "userGroup": userGroup,
            "currentUser": currentUser,
            "existFollower": existFollower,
            "articles": articles,
            "questions": questions,
            "followers": followers,
            "followings": followings,
            "articleCategories": articleCategories,
            "articleSubCategories": articleSubCategories,
            "articleLowerCategories": articleLowerCategories,
            "questionCategories": questionCategories,
            "questionSubCategories": questionSubCategories,
            "questionLowerCategories": questionLowerCategories,
        }
        return render(request, "ankades/account/account-detail.html", context)
    except:
        messages.error(request, "Böyle bir kullanıcı bulunamadı.")
        return render(request, "404.html")


def get_user_follower(request, username, userDetail):
    isFollowerExist = False
    try:
        AccountFollower.objects.get(followerId__username=username, followingId__username=userDetail)
        isFollowerExist = True
        return isFollowerExist
    except:
        return isFollowerExist


@login_required(login_url="login_account")
def follow_account(request, username):
    currentUser = request.user
    try:
        getFollowing = Account.objects.get(username=username)
        try:
            instance = AccountFollower.objects.get(followerId__username=currentUser,
                                                   followingId__username=getFollowing.username)
            instance.delete()
            return redirect(reverse("account_detail", kwargs={"username": getFollowing.username}))
        except:
            new_follower = AccountFollower()
            new_follower.followerId = currentUser
            new_follower.followingId = getFollowing
            new_follower.save()
            messages.success(request,
                             str(new_follower.followingId.get_full_name() + " kullanıcısını takip etmeye başladınız."))
            return redirect(reverse("account_detail", kwargs={"username": getFollowing.username}))
    except:
        messages.error(request, "Böyle bir kullanıcı bulunamadı.")
        return render(request, "404.html")


def login_account(request):
    """
    :param request:
    :return:
    """
    activity = AccountLogs()
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            remember = request.POST.get("remember")
            try:
                get_user = Account.objects.get(username=username.lower())
                if not get_user.is_active:
                    messages.error(request, "Kullanıcı engelli olduğu için giriş yapılamadı.")
                    return redirect("login_account")
            except Account.DoesNotExist:
                messages.error(request, "Böyle bir kullanıcı bulunamadı.")
                return redirect("login_account")
            user = authenticate(username=username.lower(), password=password)
            if user:
                login(request, user)
            else:
                messages.error(request, "Şifre hatalı.")
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
    activity = AccountLogs()
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
        activity = AccountLogs()
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            context = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
            }
            if password and confirm_password and password != confirm_password:
                messages.error(request, "Şifreler uyuşmuyor. Lütfen tekrar deneyin.")
                return render(request, "ankades/registration/register.html", context)
            elif not username.isalnum():
                messages.error(request, "Kullanıcı adı sadece harf ve rakamlardan oluşmalıdır, boşluk veya noktalama işaretleri kullanılamaz.")
                return render(request, "ankades/registration/register.html", context)
            elif Account.objects.filter(email=email):
                messages.error(request, "Bu email adresinde kullanıcı mevcut")
                return render(request, "ankades/registration/register.html", context)
            elif Account.objects.filter(username=username):
                messages.error(request, "Bu kullanıcı adı sistemimizde mevcut")
                return render(request, "ankades/registration/register.html", context)
            else:
                new_user = Account(first_name=first_name, last_name=last_name, email=email)
                new_user.username = username.lower()
                new_user.is_active = True
                new_user.save()
                new_user.set_password(password)
                new_user.save()
                getGroup = Group.objects.get(slug="uye")
                new_group = AccountGroup(userId=new_user, groupId=getGroup)
                new_group.save()
                activity.title = "Kayıt Olma"
                activity.application = "ACCOUNT"
                activity.method = "POST"
                activity.creator = new_user
                activity.createdDate = datetime.datetime.now()
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı kayıt oldu."
                activity.save()
                user = authenticate(username=username.lower(), password=request.POST.get("password"))
                login(request, user)
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
    articleCategories = ArticleCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    context = {
        "userDetail": userDetail,
        "userGroup": userGroup,
        "currentUser": currentUser,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
    }
    return render(request, "ankades/account/account-profile.html", context)


def current_user_group(self, username):
    try:
        group = AccountGroup.objects.get(userId__username=username)
        return str(group.groupId)
    except:
        group = None
        return group


def user_group(self, username):
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
#         AccountLogs = AccountLogs.objects.get(creator__username=username)
#         context = {
#             "currentUser": currentUser,
#             "userGroup": userGroup,
#             "AccountLogs": AccountLogs,
#         }
#         return render(request, "ankades/account/timeline.html", context)
#     except:
#         messages.error(request, "Kullanıcı bulunamadı.")
#         return render(request, "404.html")
