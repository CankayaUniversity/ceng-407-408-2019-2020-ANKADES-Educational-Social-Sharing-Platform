from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

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
    articleCategories = ArticleCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    articleSubCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    articleLowerCategories = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    questionCategories = QuestionCategory.objects.filter(
        Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True))
    questionSubCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=True))
    questionLowerCategories = QuestionCategory.objects.filter(Q(isActive=True, isRoot=False, isCategory=False))
    userGroup = current_user_group(request, request.user)
    instance = get_object_or_404(Account, username=request.user)
    activity = AccountLogs()
    sm = SocialMedia.objects.all()
    try:
        accountSocialMedia = AccountSocialMedia.objects.get(userId__username=request.user.username)
    except:
        accountSocialMedia = None
    context = {
        "articleCategories": articleCategories,
        "articleSubCategories": articleSubCategories,
        "articleLowerCategories": articleLowerCategories,
        "questionCategories": questionCategories,
        "questionSubCategories": questionSubCategories,
        "questionLowerCategories": questionLowerCategories,
        "instance": instance,
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
        activity.creator = request.user
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı adını/soyadını güncelledi."
        activity.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect("edit_profile")
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_profile_photo(request):
    try:
        instance = Account.objects.get(username=request.user.username)
        if request.method == "POST":
            if request.FILES:
                if instance.image:
                    instance.image = None
                image = request.FILES.get('image')
                fs = FileSystemStorage()
                fs.save(image.name, image)
                instance.image = image
                instance.save()
        return redirect('/ayarlar/')
    except:
        messages.error(request, "Kullanıcı bulunamadı.")
        return redirect('/ayarlar/')


@login_required(login_url="login_admin")
def add_social_media_to_user(request):
    activity = AccountLogs()
    if request.method == "POST":
        facebook = request.POST.get('facebook')
        linkedin = request.POST.get('linkedin')
        if facebook:
            fb = get_social_media(request, 'facebook')
            new_fb = AccountSocialMedia(userId=request.user, socialMediaId=fb)
            new_fb.url = "https://facebook.com/" + str(facebook)
            new_fb.socialMediaUsername = str(facebook)
            new_fb.save()
        if linkedin:
            linked = get_social_media(request, 'linkedin')
            new_linkedIn = AccountSocialMedia(userId=request.user, socialMediaId=linked)
            new_linkedIn.url = "https://linkedin.com/" + str(linkedin)
            new_linkedIn.save()
        activity.title = "Sosyal Medya Hesabı Ekleme."
        activity.application = "Account"
        activity.method = "POST"
        activity.creator = request.user
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı sosyal medya hesabı ekledi."
        activity.save()
        messages.success(request, "Değişiklikler başarıyla kaydedildi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_username(request):
    """
    :param request:
    :return:
    """
    instance = get_object_or_404(Account, username=request.user)
    activity = AccountLogs()
    if request.method == "POST":
        username = request.POST.get("username")
        instance.username = username
        instance.save()
        activity.title = "Kullanıcı Adı Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = request.user
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı kullanıcı adını güncelledi."
        activity.save()
        messages.success(request, "Kullanıcı adı başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_password(request):
    try:
        instance = Account.objects.get(username=request.user)
        currentPassword = instance.password
        activity = AccountLogs()
        if request.method == "POST":
            old_password = request.POST.get('old_password')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            check_old = check_password(old_password, currentPassword)
            if not check_old:
                messages.error(request, "Eski şifrenizi yanlış girdiniz. Lütfen tekrar deneyin.")
                return redirect('/ayarlar/')
            elif password and confirm_password and password != confirm_password:
                messages.error(request, "Şifreler uyuşmuyor. Lütfen tekrar deneyin.")
                return redirect('/ayarlar/')
            else:
                update_session_auth_hash(request, request.user)
                request.user.set_password(password)
                request.user.save()
                login_user = authenticate(username=request.user, password=password)
                login(request, login_user)
                activity.title = "Şifre Güncelleme."
                activity.application = "Account"
                activity.method = "UPDATE"
                activity.creator = request.user
                activity.createdDate = datetime.datetime.now()
                activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı şifresini güncelledi."
                activity.save()
                messages.success(request, "Şifreniz başarıyla güncellendi.")
                return redirect('/ayarlar/')
        return redirect('/ayarlar/')
    except:
        messages.error(request, "Kullanıcı bulunamadı.")
        return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_email(request):
    """
    :param request:
    :return:
    """
    instance = get_object_or_404(Account, username=request.user)
    activity = AccountLogs()
    if request.method == "POST":
        email = request.POST.get("email")
        instance.email = email
        instance.save()
        activity.title = "Email Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = request.user
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı email adresini güncelledi."
        activity.save()
        messages.success(request, "Email başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_graduate(request):
    """
    :param request:
    :return:
    """
    instance = get_object_or_404(Account, username=request.user)
    activity = AccountLogs()
    if request.method == "POST":
        graduate = request.POST.get("graduate")
        instance.graduate = graduate
        instance.save()
        activity.title = "Okul Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = request.user
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı okulunu güncelledi."
        activity.save()
        messages.success(request, "Okulunuz başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_bio(request):
    """
    :param request:
    :return:
    """
    instance = get_object_or_404(Account, username=request.user)
    activity = AccountLogs()
    if request.method == "POST":
        bio = request.POST.get("bio")
        instance.bio = bio
        instance.save()
        activity.title = "Biyografi Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = request.user
        activity.createdDate = datetime.datetime.now()
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı biyografisini güncelledi."
        activity.save()
        messages.success(request, "Biyografiniz başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')