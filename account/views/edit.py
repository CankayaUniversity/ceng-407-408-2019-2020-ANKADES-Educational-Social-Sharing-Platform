from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.models import Account, AccountActivity, AccountSocialMedia, SocialMedia
from account.views.views import current_user_group, get_social_media


@login_required(login_url="login_account")
def edit_profile(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    sm = SocialMedia.objects.all()
    try:
        accountSocialMedia = AccountSocialMedia.objects.get(userId__username=currentUser.username)
    except:
        accountSocialMedia = None
    context = {
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
        if request.FILES:
            media = request.FILES.get('media')
            fs = FileSystemStorage()
            fs.save(media.name, media)
            instance.image = media
        instance.save()
        activity.title = "Profil Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı hesabını güncelledi."
        activity.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect("edit_profile")
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_admin")
def add_social_media_to_user(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    sm = SocialMedia.objects.all()
    try:
        accountSocialMedia = AccountSocialMedia.objects.get(userId__username=currentUser)
    except:
        accountSocialMedia = None
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
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
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    if request.method == "POST":
        username = request.POST.get("username")
        instance.username = username
        instance.save()
        activity.title = "KUllanıcı Adı Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı kullanıcı adını güncelledi."
        activity.save()
        messages.success(request, "Kullanıcı adı başarıyla güncellendi.")
        return render(request, "ankades/account/edit-profile.html", {'active_tab': 'username'})
    context = {
        "instance": instance,
        "currentUser": currentUser,
        "userGroup": userGroup,
        "active_tab": 'username',
    }
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_password(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    currentPassword = instance.password
    activity = AccountActivity()
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
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
            activity.description = str(activity.createdDate) + " tarihinde, " + str(
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
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    if request.method == "POST":
        email = request.POST.get("email")
        instance.email = email
        instance.save()
        activity.title = "Email Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı email adresini güncelledi."
        activity.save()
        messages.success(request, "Email başarıyla güncellendi.")
        return render(request, "ankades/account/edit-profile.html", {'active_tab': 'email'})
    context = {
        "instance": instance,
        "currentUser": currentUser.username,
        "userGroup": userGroup,
    }
    return render(request, "ankades/account/edit-profile.html", context)
