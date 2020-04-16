import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.models import Group
from ankadescankaya.views import current_user_group
from adminpanel.forms import AdminEditGroupForm


@login_required(login_url="login_admin")
def admin_all_groups(request, slug=None):
    """
    :param slug:
    :param request:
    :return:
    """
    userGroup = 'Kullanıcı'
    if request.user.is_authenticated:
        userGroup = current_user_group(request, request.user)
    groups = Group.objects.all()
    context = {
        "groups": groups,
        "userGroup": userGroup,
    }
    if userGroup == 'admin':
        if request.method == "POST":
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == 'on'
            new_group = Group(title=title, isActive=isActive)
            new_group.save()
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
    form = AdminEditGroupForm(request.POST or None, instance=instance)
    context = {
        "form": form,
    }
    if form.is_valid():
        title = form.cleaned_data.get("title")
    if request.method == "POST":
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Grup başarıyla düzenlendi.")
        return render(request, "adminpanel/group/edit-group.html", {'form': form})
    return redirect("admin_edit_group")


@login_required(login_url="login_admin")
def admin_add_group(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        if request.method == "POST":
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == 'on'
            new_group = Group(title=title, isActive=isActive)
            new_group.save()
            messages.success(request, "Grup başarıyla oluşturuldu.")
            return redirect("admin_all_groups")
        context = {
            "userGroup": userGroup,
        }
        return render(request, "adminpanel/group/add-group.html", context)
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_delete_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    try:
        instance = Group.objects.get(slug=slug)
        if userGroup == 'admin':
            instance.delete()
            messages.success(request, "Grup başarıyla silindi.")
            return redirect("admin_all_groups")
        else:
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
    userGroup = current_user_group(request, request.user)
    try:
        instance = get_object_or_404(Group, slug=slug)
        if userGroup == 'admin':
            if instance.isActive:
                instance.updatedDate = datetime.datetime.now()
                instance.isActive = False
                instance.save()
                messages.success(request, "Group artık aktif değil.")
                return redirect("admin_all_groups")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Group aktifleştirildi.")
                return redirect("admin_all_groups")
        else:
            messages.error(request, "Yetkiniz yok.")
            return redirect("admin_all_groups")
    except:
        messages.error(request, "Böyle bir grup bulunamadı.")
        return redirect("admin_all_groups")

