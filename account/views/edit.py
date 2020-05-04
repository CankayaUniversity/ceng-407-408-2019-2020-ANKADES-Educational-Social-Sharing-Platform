from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import Account, AccountSocialMedia, SocialMedia, AccountFollower, AccountZone
from account.views.views import get_social_media, get_user_follower
from ankadescankaya.views import Categories
from ankadescankaya.views import current_user_group


@login_required(login_url="login_account")
def edit_profile(request):
    """
    :param request:
    :return:
    """
    categories = Categories.all_categories()
    userGroup = current_user_group(request, request.user)
    instance = get_object_or_404(Account, username=request.user)
    existFollower = get_user_follower(request, request.user, instance)
    followers = AccountFollower.objects.filter(followingId__username=instance.username)
    followings = AccountFollower.objects.filter(followerId__username=instance.username)
    sm = SocialMedia.objects.all()
    try:
        accountSocialMedia = AccountSocialMedia.objects.get(userId__username=request.user.username)
    except:
        accountSocialMedia = None
    context = {
        "instance": instance,
        "userGroup": userGroup,
        "sm": sm,
        "accountSocialMedia": accountSocialMedia,
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
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        instance.first_name = first_name
        instance.last_name = last_name
        instance.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect("edit_profile")
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_profile_photo(request):
    """
    :param request:
    :return:
    """
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
        return redirect('/ayarlar/')
    except:
        return redirect("404")


@login_required(login_url="login_admin")
def add_social_media_to_user(request):
    """
    :param request:
    :return:
    """
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
    if request.method == "POST":
        username = request.POST.get("username")
        instance.username = username
        instance.save()
        messages.success(request, "Kullanıcı adı başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_password(request):
    """
    :param request:
    :return:
    """
    try:
        instance = Account.objects.get(username=request.user)
        currentPassword = instance.password
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
                messages.success(request, "Şifreniz başarıyla güncellendi.")
                return redirect('/ayarlar/')
        return redirect('/ayarlar/')
    except:
        return redirect("404")


@login_required(login_url="login_account")
def edit_email(request):
    """
    :param request:
    :return:
    """
    instance = get_object_or_404(Account, username=request.user)
    if request.method == "POST":
        email = request.POST.get("email")
        instance.email = email
        instance.save()
        messages.success(request, "Email başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_graduate(request):
    """
    :param request:
    :return:
    """
    active = "edit_graduate"
    instance = get_object_or_404(Account, username=request.user)
    if request.method == "POST":
        graduate = request.POST.get("graduate")
        instance.graduate = graduate
        instance.save()
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
    if request.method == "POST":
        bio = request.POST.get("bio")
        instance.bio = bio
        instance.save()
        messages.success(request, "Biyografiniz başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_zone(request):
    """
    :param request:
    :return:
    """
    try:
        instance = Account.objects.get(username=request.user)
        zone = AccountZone.objects.filter(userId__username=instance.username)
        if request.method == "POST":
            zone = request.POST.get("zone")
            instance.zone = zone
            instance.save()
            messages.success(request, "Yaşadığınız şehir başarıyla güncellendi.")
            return redirect('/ayarlar/')
        return redirect('/ayarlar/')
    except:
        messages.error(request, "Bir sorun oluştu. Lütfen daha sonra tekrar deneyin.")
        return redirect('/ayarlar/')


@login_required(login_url="login_account")
def edit_cv(request):
    """
    :param request:
    :return:
    """
    instance = get_object_or_404(Account, username=request.user)
    if request.method == "POST":
        cv = request.POST.get("cv")
        instance.cv = cv
        instance.save()
        messages.success(request, "Yetenekleriniz başarıyla güncellendi.")
        return redirect('/ayarlar/')
    return redirect('/ayarlar/')
