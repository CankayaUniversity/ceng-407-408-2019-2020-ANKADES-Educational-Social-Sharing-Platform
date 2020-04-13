from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.forms import EditProfileForm
from account.models import Account, AccountLogs, AccountSocialMedia, SocialMedia
from account.views.views import current_user_group, get_social_media

import datetime

from article.models import ArticleCategory
from question.models import QuestionCategory


@login_required(login_url="login_account")
def edit_profile(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    articleCategories = ArticleCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    userGroup = current_user_group(request, currentUser)
    userDetail = currentUser
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountLogs()
    sm = SocialMedia.objects.all()
    try:
        accountSocialMedia = AccountSocialMedia.objects.get(userId__username=currentUser.username)
    except:
        accountSocialMedia = None
    context = {
        "userDetail": userDetail,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
        "instance": instance,
        "currentUser": currentUser,
        "userGroup": userGroup,
        "sm": sm,
        "accountSocialMedia": accountSocialMedia,
    }
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        instance.first_name = first_name
        instance.last_name = last_name
        instance.save()
        activity.title = "Profil Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı hesabını güncelledi."
        activity.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect("edit_profile")
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_profile_photo(request):
    currentUser = request.user
    try:
        instance = Account.objects.get(username=currentUser)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                return redirect(reverse("account_detail", kwargs={"username": currentUser}))
        else:
            form = EditProfileForm()
        return render(request, 'ankades/account/edit-profile.html', {"form": form})
    except:
        messages.error(request, "Giriş yapmalısınız.")
        return redirect("index")


@login_required(login_url="login_admin")
def add_social_media_to_user(request):
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
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountLogs()
    sm = SocialMedia.objects.all()
    try:
        accountSocialMedia = AccountSocialMedia.objects.get(userId__username=currentUser)
    except:
        accountSocialMedia = None
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
        "instance": instance,
        "sm": sm,
        "accountSocialMedia": accountSocialMedia,
    }
    if request.method == "POST":
        facebook = request.POST.get('facebook')
        if facebook:
            fb = get_social_media(request, 'facebook')
            new_fb = AccountSocialMedia(userId=currentUser, socialMediaId_id=fb, url=facebook)
            new_fb.save()
        twitter = request.POST.get('twitter')
        if twitter:
            tw = get_social_media(request, 'twitter')
            new_tw = AccountSocialMedia(userId=currentUser, socialMediaId_id=tw, url=twitter)
            new_tw.save()
        youtube = request.POST.get('youtube')
        if youtube:
            yt = get_social_media(request, 'youtube')
            new_yt = AccountSocialMedia(userId=currentUser, socialMediaId_id=yt, url=youtube)
            new_yt.save()
        github = request.POST.get('github')
        if github:
            git = get_social_media(request, 'github')
            new_git = AccountSocialMedia(userId=currentUser, socialMediaId_id=git, url=github)
            new_git.save()
        bitbucket = request.POST.get('bitbucket')
        medium = request.POST.get('medium')
        google_drive = request.POST.get('google_drive')
        linkedin = request.POST.get('linkedin')
        udemy = request.POST.get('udemy')
        activity.title = "Sosyal Medya Hesabı Ekleme."
        activity.application = "Account"
        activity.method = "POST"
        activity.creator = currentUser
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı sosyal medya hesabı ekledi."
        activity.save()
        messages.success(request, "Değişiklikler başarıyla kaydedildi.")
        return redirect("index")
        # return redirect("index")
        # return render(request, "ankades/account/edit-profile.html", {'active_tab': 'socialmedia'})
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_username(request):
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
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountLogs()
    getFollower = Account.objects.all()
    if request.method == "POST":
        username = request.POST.get("username")
        instance.username = username
        instance.save()
        activity.title = "KUllanıcı Adı Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı kullanıcı adını güncelledi."
        activity.save()
        messages.success(request, "Kullanıcı adı başarıyla güncellendi.")
        return render(request, "ankades/account/edit-profile.html", {'active_tab': 'username'})
    context = {
        "instance": instance,
        "getFollower": getFollower,
        "currentUser": currentUser,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
        "userGroup": userGroup,
        "active_tab": 'username',
    }
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_password(request):
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
    instance = get_object_or_404(Account, username=currentUser)
    currentPassword = instance.password
    activity = AccountLogs()
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
        "instance": instance,
    }
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        check_old = check_password(old_password, currentPassword)
        if not check_old:
            messages.error(request, "Eski şifrenizi yanlış girdiniz. Lütfen tekrar deneyin.")
            return render(request, "ankades/account/edit-profile.html", {'active_tab': 'password'})
        elif password and confirm_password and password != confirm_password:
            messages.error(request, "Şifreler uyuşmuyor. Lütfen tekrar deneyin.")
            return render(request, "ankades/account/edit-profile.html", {'active_tab': 'password'})
        else:
            update_session_auth_hash(request, currentUser)
            currentUser.set_password(password)
            currentUser.save()
            login_user = authenticate(username=currentUser, password=password)
            login(request, login_user)
            activity.title = "Parola Güncelleme."
            activity.application = "Account"
            activity.method = "UPDATE"
            activity.creator = currentUser
            activity.createdDate = datetime.datetime.now()
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı parolasını güncelledi."
            activity.save()
            messages.success(request, "Şifreniz başarıyla güncellendi.")
            return redirect("index")
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_email(request):
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
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountLogs()
    if request.method == "POST":
        email = request.POST.get("email")
        instance.email = email
        instance.save()
        activity.title = "Email Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı email adresini güncelledi."
        activity.save()
        messages.success(request, "Email başarıyla güncellendi.")
        return render(request, "ankades/account/edit-profile.html", {'active_tab': 'email'})
    context = {
        "instance": instance,
        "currentUser": currentUser.username,
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
        "userGroup": userGroup,
    }
    return render(request, "ankades/account/edit-profile.html", context)
