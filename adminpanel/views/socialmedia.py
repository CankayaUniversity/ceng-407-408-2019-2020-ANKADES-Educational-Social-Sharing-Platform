import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.models import SocialMedia
from ankadescankaya.views.views import current_user_group


@login_required(login_url="login_admin")
def admin_all_social_medias(request):
    socialMedias = SocialMedia.objects.all()
    userGroup = current_user_group(request, request.user)
    context = {
        "socialMedias": socialMedias,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/social-medias.html", context)


@login_required(login_url="login_admin")
def admin_isactive_socialmedia(request, slug):
    instance = get_object_or_404(SocialMedia, slug=slug)
    if instance.isActive is True:
        instance.isActive = False
        instance.save()
        messages.success(request, "Makale kategorisi artık aktif değil.")
        return redirect("admin_all_social_medias")
    else:
        instance.isActive = True
        instance.save()
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
    userGroup = current_user_group(request, request.user)
    instance = get_object_or_404(SocialMedia, slug=slug)
    if request.method == "POST" and request.FILES['media']:
        title = request.POST.get('title')
        isActive = request.POST.get("isActive") == 'on'
        instance.title = title
        instance.isActive = isActive
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Sosyal Medya başarıyla güncellendi.")
        return redirect("admin_all_social_medias")
    context = {
        "instance": instance,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/edit-social-media.html", context)


@login_required(login_url="login_admin")
def admin_add_social_media(request):
    userGroup = current_user_group(request, request.user)
    if request.method == "POST" and request.FILES['media']:
        title = request.POST.get("title")
        url = request.POST.get("url")
        isActive = request.POST.get("isActive") == 'on'
        if SocialMedia.objects.filter(title=title):
            messages.error(request, "Bu sosyal medya daha önce eklenmiş")
            return redirect("admin_add_social_media")
        else:
            new_sm = SocialMedia(title=title, isActive=isActive, url=url)
            new_sm.save()
            messages.success(request, "Sosyal Medya kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("admin_all_social_medias")
    context = {
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/social-media/add-social-media.html", context)