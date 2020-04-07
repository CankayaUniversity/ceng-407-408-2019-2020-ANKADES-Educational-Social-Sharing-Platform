import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.models import SocialMedia
from account.views.views import current_user_group
from adminpanel.models import AdminActivity


@login_required(login_url="login_admin")
def admin_all_social_medias(request):
    socialMedias = SocialMedia.objects.all()
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "socialMedias": socialMedias,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/social-medias.html", context)


@login_required(login_url="login_admin")
def admin_isactive_socialmedia(request, slug):
    instance = get_object_or_404(SocialMedia, slug=slug)
    currentUser = request.user
    activity = AdminActivity()
    if instance.isActive is True:
        instance.isActive = False
        instance.save()
        activity.title = "Sosyal Medya Aktifleştirme: " + str(currentUser)
        activity.application = "SocialMedia"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı sosyal medya aktifliğini kaldırdı."
        activity.save()
        messages.success(request, "Makale kategorisi artık aktif değil.")
        return redirect("admin_all_social_medias")
    else:
        instance.isActive = True
        instance.save()
        activity.title = "Sosyal Medya Aktifleştirme: " + str(currentUser)
        activity.application = "SocialMedia"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı sosyal medya güncelledi."
        activity.save()
        messages.success(request, "Makale kategorisi başarıyla aktifleştirildi.")
        return redirect("admin_all_social_medias")


@login_required(login_url="login_admin")
def admin_delete_socialmedia(request, slug):
    instance = get_object_or_404(SocialMedia, slug=slug)
    if instance.isActive is True:
        messages.error(request, "Makale kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
        return redirect("admin_all_social_medias")
    else:
        instance.delete()
        messages.success(request, "Makale kategorisi başarıyla silindi.")
        return redirect("admin_all_social_medias")


@login_required(login_url="login_admin")
def admin_edit_social_media(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(SocialMedia, slug=slug)
    activity = AdminActivity()
    if request.method == "POST" and request.FILES['media']:
        title = request.POST.get('title')
        isActive = request.POST.get("isActive") == 'on'
        media = request.FILES['media']
        instance.title = title
        instance.isActive = isActive
        instance.media = media
        fs = FileSystemStorage()
        fs.save(media.name, media)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        activity.title = "Sosyal Medya Güncelleme: " + str(currentUser)
        activity.application = "SocialMedia"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı sosyal medya güncelledi."
        activity.save()
        messages.success(request, "Sosyal Medya başarıyla güncellendi.")
        return redirect("admin_all_social_medias")
    context = {
        "instance": instance,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/edit-social-media.html", context)


@login_required(login_url="login_admin")
def admin_add_social_media(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    if request.method == "POST" and request.FILES['media']:
        title = request.POST.get("title")
        isActive = request.POST.get("isActive") == 'on'
        media = request.FILES['media']
        fs = FileSystemStorage()
        fs.save(media.name, media)
        if SocialMedia.objects.filter(title=title):
            activity.title = "Sosyal Medya Ekleme: " + str(currentUser)
            activity.application = "SocialMedia"
            activity.createdDate = datetime.datetime.now()
            activity.method = "INSERT"
            activity.creator = currentUser
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı sosyal medya ekledi."
            activity.save()
            messages.error(request, "Bu sosyal medya daha önce eklenmiş")
            return redirect("admin_add_social_media")
        else:
            new_sm = SocialMedia(title=title, media=media, isActive=isActive)
            new_sm.save()
            activity.title = "Sosyal Medya Güncelleme: " + str(currentUser)
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = currentUser
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı sosyal medya güncelledi."
            activity.save()
            messages.success(request, "Sosyal Medya kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("admin_all_social_medias")
    context = {
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/add-social-media.html", context)