import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from account.models import Permission
from ankadescankaya.views import current_user_group


@login_required(login_url="login_admin")
def admin_all_permissions(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    permissions = Permission.objects.all()
    context = {
        "userGroup": userGroup,
        "permissions": permissions,
    }
    return render(request, "adminpanel/permissions/all-permissions.html", context)


@login_required(login_url="login_admin")
def admin_add_permission(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        if request.method == "POST":
            title = request.POST.get("title")
            slug = request.POST.get("slug")
            description = request.POST.get("description")
            isActive = request.POST.get("isActive") == 'on'
            new_group = Permission(title=title, description=description, isActive=isActive, slug=slug)
            new_group.save()
            messages.success(request, "İzin başarıyla oluşturuldu.")
            return redirect("admin_all_permissions")
        context = {
            "userGroup": userGroup,
        }
        return render(request, "adminpanel/permission/add-permission.html", context)
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_delete_permission(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        try:
            instance = get_object_or_404(Permission, slug=slug)
            instance.isActive = False
            messages.success(request, "İzin başarıyla silindi.")
            return redirect("admin_all_permissions")
        except:
            messages.error(request, "İzin bulunamadı")
            return redirect("admin_all_permissions")
    else:
        messages.error(request, "Yetkiniz yok !")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_isactive_permission(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    try:
        instance = Permission.objects.get(slug=slug)
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
                messages.success(request, "İzin aktifleştirildi.")
                return redirect("admin_all_groups")
        else:
            messages.error(request, "Yetkiniz yok.")
            return redirect("admin_all_groups")
    except:
        messages.error(request, "Böyle bir izin bulunamadı")
        return redirect("admin_all_permissions")
