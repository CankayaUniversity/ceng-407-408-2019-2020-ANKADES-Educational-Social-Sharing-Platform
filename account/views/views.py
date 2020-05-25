from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.models import Account, Group, AccountGroup, AccountSocialMedia, AccountPermission, SocialMedia, AccountFollower
from adminpanel.views.article import ArticleCategoryView
from ankadescankaya.views.views import Categories, current_user_group
from article.models import Article
from course.models import Course
from exam.models import Exam
from question.models import Question, QuestionComment


def index(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        instance = Account.objects.get(username=request.user.username)
        existFollower = get_user_follower(request, request.user, instance)
        followers = AccountFollower.objects.filter(followingId__username=instance.username)  # takipçiler
        followings = AccountFollower.objects.filter(followerId__username=request.user.username)  # takip edilen
    except:
        instance = None
        existFollower = None
        followers = None
        followings = None
    page = request.GET.get('page', 1)
    articles = Article.objects.filter(isActive=True)
    questions = Question.objects.filter(isActive=True)
    paginator = Paginator(articles, 12)
    try:
        article_pagination = paginator.page(page)
    except PageNotAnInteger:
        article_pagination = paginator.page(1)
    except EmptyPage:
        article_pagination = paginator.page(paginator.num_pages)
    context = {
        "articles": articles,
        "article_pagination": article_pagination,
        "questions": questions,
        "userGroup": userGroup,
        "existFollower": existFollower,
        "followers": followers,
        "followings": followings,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    return render(request, "ankades/index.html", context)


def account_detail(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    try:
        instance = Account.objects.get(username=username)
    except:
        messages.error(request, "Böyle bir kullanıcı bulunamadı.")
        return redirect("404")
    userGroup = current_user_group(request, request.user)
    userDetailGroup = user_group(request, username)
    existFollower = get_user_follower(request, request.user, instance)
    followers = AccountFollower.objects.filter(followingId__username=instance.username)
    followings = AccountFollower.objects.filter(followerId__username=instance.username)
    getFollowerForFollow = get_user_follower(request, request.user, followers)
    getFollowingForFollow = get_user_follower(request, request.user, followings)
    articles = user_articles(request, username).order_by('-createdDate__day')
    questions = user_questions(request, username).order_by('-createdDate__day')
    courses = user_courses(request, username).order_by('-createdDate__day')
    exams = user_exams(request, username)
    certifiedAnswersCount = QuestionComment.objects.filter(creator=instance, isCertified=True, isActive=True)
    context = {
        "instance": instance,
        "userDetailGroup": userDetailGroup,
        "userGroup": userGroup,
        "existFollower": existFollower,
        "getFollowerForFollow": getFollowerForFollow,
        "getFollowingForFollow": getFollowingForFollow,
        "articles": articles,
        "questions": questions,
        "courses": courses,
        "exams": exams,
        "certifiedAnswersCount": certifiedAnswersCount,
        "followers": followers,
        "followings": followings,
    }
    return render(request, "ankacademy/account/account-detail.html", context)


def get_user_follower(request, username, userDetail):
    """
    :param request:
    :param username:
    :param userDetail:
    :return:
    """
    isFollowerExist = False
    try:
        AccountFollower.objects.get(followerId__username=username, followingId__username=userDetail)
        isFollowerExist = True
        return isFollowerExist
    except:
        return isFollowerExist


@login_required(login_url="login_account")
def follow_account(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    try:
        getFollowing = Account.objects.get(username=username)
        try:
            instance = AccountFollower.objects.get(followerId__username=request.user,
                                                   followingId__username=getFollowing.username)
            instance.delete()
            messages.success(request, instance.followingId.get_full_name() + "  kullanıcısını takipten çıktınız.")
            return redirect(reverse("account_detail", kwargs={"username": getFollowing.username}))
        except:
            new_follower = AccountFollower()
            new_follower.followerId = request.user
            new_follower.followingId = getFollowing
            new_follower.save()
            messages.success(request,
                             str(new_follower.followingId.get_full_name() + " kullanıcısını takip etmeye başladınız."))
            return redirect(reverse("account_detail", kwargs={"username": getFollowing.username}))
    except:
        return redirect("404")


def login_account(request):
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
            messages.success(request, "Başarıyla giriş yapıldı.")
            return redirect("index")
        return render(request, "ankacademy/registration/login.html")
    else:
        messages.warning(request, "Zaten giriş yapılmış.")
        return redirect("index")


@login_required(login_url="login_account")
def logout_account(request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        logout(request)
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
                return render(request, "ankacademy/registration/register.html", context)
            elif not username.isalnum():
                messages.error(request, "Kullanıcı adı sadece harf ve rakamlardan oluşmalıdır, boşluk veya noktalama işaretleri kullanılamaz.")
                return render(request, "ankacademy/registration/register.html", context)
            elif Account.objects.filter(email=email):
                messages.error(request, "Bu email adresinde kullanıcı mevcut")
                return render(request, "ankacademy/registration/register.html", context)
            elif Account.objects.filter(username=username):
                messages.error(request, "Bu kullanıcı adı sistemimizde mevcut")
                return render(request, "ankacademy/registration/register.html", context)
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
                user = authenticate(username=username.lower(), password=request.POST.get("password"))
                login(request, user)
            messages.success(request, "Kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("login_account")
        return render(request, "ankacademy/registration/register.html")
    else:
        messages.error(request, "Zaten giriş yapılmış.")
        return redirect("index")


def get_requested_user(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    userGroup = current_user_group(request, username)
    categories = Categories.all_categories()
    try:
        userDetail = Account.objects.get(username=username)
        context = {
            "userDetail": userDetail,
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/account/account-profile.html", context)
    except:
        return redirect("404")


def user_group(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        group = AccountGroup.objects.get(userId__username=username)
        return str(group.groupId)
    except:
        group = None
        return group


def current_user_permission(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        userPermission = AccountPermission.objects.get(userId__username=username)
        return str(userPermission.permissionId)
    except:
        userPermission = None
        return userPermission


def user_social_media(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        usm = AccountSocialMedia.objects.get(userId__username=username)
        return str(usm)
    except:
        usm = None
        return usm


def user_articles(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        articles = Article.objects.filter(creator__username=username, isActive=True)
        return articles
    except:
        articles = None
        return articles


def user_questions(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        questions = Question.objects.filter(creator__username=username, isActive=True)
        return questions
    except:
        questions = None
        return questions


def user_courses(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        courses = Course.objects.filter(creator__username=username, isActive=True)
        return courses
    except:
        courses = None
        return courses


def user_exams(self, username):
    """
    :param self:
    :param username:
    :return:
    """
    try:
        account = Account.objects.get(username=username)
        exams = Exam.objects.filter(Q(creator__username=account, isActive=True) | Q(owner=account.get_full_name())).order_by('-createdDate__day')
        return exams
    except:
        exams = None
        return exams


def get_social_media(self, slug):
    """
    :param self:
    :param slug:
    :return:
    """
    try:
        socialMedia = get_object_or_404(SocialMedia, slug=slug)
        return socialMedia
    except:
        socialMedia = None
        return socialMedia


# def get_user_timeline(request, username):
#     userGroup = current_user_group(request, request.user)
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
