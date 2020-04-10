import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.models import Group
from account.views.views import current_user_group
from adminpanel.forms import AdminEditGroupForm
from adminpanel.models import AdminLogs


@login_required(login_url="login_admin")
def admin_all_groups(request, slug=None):
    """
    :param slug:
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = 'Kullanıcı'
    activity = AdminLogs()
    if request.user.is_authenticated:
        userGroup = current_user_group(request, currentUser)
    groups = Group.objects.all()
    context = {
        "groups": groups,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    if userGroup == 'admin':
        if request.method == "POST":
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == 'on'
            new_group = Group(title=title, isActive=isActive)
            new_group.save()
            activity.title = "Grup Oluşturma"
            activity.method = "POST"
            activity.creator = currentUser
            activity.application = "Group"
            activity.createdDate = datetime.datetime.now()
            activity.description = "Yeni bir grup oluşturuldu. İşlemi yapan kişi: " + str(
                activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.success(request, "Grup başarıyla oluşturuldu.")
            return redirect("admin_add_group")
        return render(request, "adminpanel/group/all-groups.html", context)
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_all_groups")


@login_required(login_url="login_admin")
def admin_edit_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    currentUser = request.user
    activity = AdminLogs()
    activity.application = "Group"
    activity.creator = currentUser
    activity.title = "Grup Düzenleme"
    activity.method = "UPDATE"
    activity.createdDate = datetime.datetime.now()
    form = AdminEditGroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        title = form.cleaned_data.get("title")
    if request.method == "POST":
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        activity.description = "Grup düzenlendi. İşlemi yapan kişi: " + str(
            activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
        activity.save()
        messages.success(request, "Grup başarıyla düzenlendi.")
        return render(request, "adminpanel/group/edit-group.html", {'form': form})
    return redirect("admin_edit_group")


@login_required(login_url="login_admin")
def admin_add_group(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminLogs()
    activity.application = "Group"
    activity.creator = currentUser
    activity.title = "Grup Ekle"
    activity.method = "POST"
    activity.createdDate = datetime.datetime.now()
    if userGroup == 'admin':
        if request.method == "POST":
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == 'on'
            new_group = Group(title=title, isActive=isActive)
            new_group.save()
            activity.description = "Yeni bir grup eklendi. İşlemi yapan kişi: " + str(activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.success(request, "Grup başarıyla oluşturuldu.")
            return redirect("admin_all_groups")
        context = {
            "userGroup": userGroup,
            "currentUser": currentUser,
        }
        return render(request, "adminpanel/group/add-group.html", context)
    else:
        activity.description = "Yeni bir grup ekleme başarısız. İşlemi yapan kişi: " + str(
            activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
        activity.save()
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_delete_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminLogs()
    activity.title = "Grup Silme"
    activity.method = "DELETE"
    activity.creator = currentUser
    activity.application = "Group"
    activity.createdDate = datetime.datetime.now()
    try:
        instance = Group.objects.get(slug=slug)
        if userGroup == 'admin':
            instance.delete()
            activity.description = "Grup silme işlemi başarıyla gerçekleştirildi. İşlemi yapan kişi: " + str(activity.creator) + ". İşleminin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.success(request, "Grup başarıyla silindi.")
            return redirect("admin_all_groups")
        else:
            activity.description = "Grup silme işlemi gerçekleştirilemedi. İşlemi yapan kişi: " + str(
                activity.creator) + ". İşleminin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.error(request, "Yetkiniz yok.")
            return redirect("admin_dashboard")
    except:
        messages.error(request, "Böyle bir grup bulunamadı.")
        return redirect("admin_all_groups")


@login_required(login_url="login_admin")
def admin_isactive_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminLogs()
    activity.title = "Grup Aktifliği Düzenleme"
    activity.method = "UPDATE"
    activity.creator = currentUser
    activity.application = "Group"
    activity.createdDate = datetime.datetime.now()
    try:
        instance = get_object_or_404(Group, slug=slug)
        if userGroup == 'admin':
            if instance.isActive:
                instance.updatedDate = datetime.datetime.now()
                instance.isActive = False
                instance.save()
                activity.description = "Grup aktifliği kaldırıldı. İşlemi yapan kişi: " + str(
                    activity.creator) + ". İşleminin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
                activity.save()
                messages.success(request, "Group artık aktif değil.")
                return redirect("admin_all_groups")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                activity.description = "Grup başarıyla aktifleştirildi. İşlemi yapan kişi: " + str(
                    activity.creator) + ". İşleminin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
                activity.save()
                messages.success(request, "Group aktifleştirildi.")
                return redirect("admin_all_groups")
        else:
            messages.error(request, "Yetkiniz yok.")
            return redirect("admin_all_groups")
    except:
        messages.error(request, "Böyle bir grup bulunamadı.")
        return redirect("admin_all_groups")

