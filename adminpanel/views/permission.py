import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from account.models import GroupPermission, Permission, AccountGroup
from adminpanel.forms import AdminPermissionForm

# Permissions Done

@login_required(login_url="login_admin")
def admin_all_permissions(request):
    """
    :param request:
    :return:
    """
    permissions = Permission.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "permissions": permissions,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/permissions/all-permissions.html", context)


@login_required(login_url="login_admin")
def admin_add_permission(request):
    """
    :param request:
    :return:
    """
    form = AdminPermissionForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "form": form,
        "adminGroup": adminGroup,
    }
    if adminGroup:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "İzin başarıyla eklendi")
            return redirect("admin_all_permissions")
        return render(request, "admin/permissions/add-permission.html", context)
    else:
        messages.error(request, "Yetkiniz Yok !")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_delete_permission(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        instance = get_object_or_404(Permission, slug=slug)
        instance.isActive = False
        messages.success(request, "İzin başarıyla silindi.")
        return redirect("admin_all_permissions")
    else:
        messages.error(request, "Yetkiniz yok !")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_edit_permission(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        instance = get_object_or_404(Permission, slug=slug)
        form = AdminPermissionForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "İzin başarıyla güncellendi.")
            return redirect("admin_all_permissions")
        return render(request, "admin/permissions/edit-main-permission.html", {"form": form})
    else:
        messages.error(request, "Yetkiniz yok !")
        return redirect("admin_index")


#Grup İzinleri
@login_required(login_url="login_admin")
def admin_site_admin_permission(request):
    """
    :param request:
    :return:
    """
    admins = GroupPermission.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "admins": admins,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/groups/group-permission/admin-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_student_permission(request):
    """
    :param request:
    :return:
    """
    students = GroupPermission.objects.filter(groupId__slug__contains="ogrenci")
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "students": students,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/groups/group-permission/student-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_teacher_permission(request):
    """
    :param request:
    :return:
    """
    teachers = GroupPermission.objects.filter(groupId__slug__contains="ogretmen")
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "teachers": teachers,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/groups/group-permission/teacher-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_moderator_permission(request):
    """
    :param request:
    :return:
    """
    moderators = GroupPermission.objects.filter(groupId__slug__contains="moderator")
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "moderators": moderators,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/groups/group-permission/moderator-permission.html", context)