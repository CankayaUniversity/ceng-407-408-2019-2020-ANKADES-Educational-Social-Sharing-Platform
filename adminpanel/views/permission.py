import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from account.models import GroupPermission, Permission
from adminpanel.forms import PermissionForm


@login_required(login_url="login_admin")
def admin_all_permissions(request):
    permissions = Permission.objects.all()
    context = {
        "permissions": permissions,
    }
    return render(request, "admin/permissions/all-permissions.html", context)


@login_required(login_url="login_admin")
def admin_add_permission(request):
    form = PermissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "İzin başarıyla eklendi")
        return redirect("admin_add_permission")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-permission.html", context)


@login_required(login_url="login_admin")
def admin_delete_permission(request, slug):
    instance = get_object_or_404(Permission, slug=slug)
    instance.isActive = False
    messages.success(request, "İzin başarıyla silindi.")
    return redirect("admin_all_permissions")


@login_required(login_url="login_admin")
def admin_edit_permission(request, slug):
    instance = get_object_or_404(Permission, slug=slug)
    form = PermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "İzin başarıyla güncellendi.")
        return redirect("admin_all_permissions")
    return render(request, "admin/permissions/edit-main-permission.html", {"form": form})


#Grup İzinleri
@login_required(login_url="login_admin")
def admin_site_admin_permission(request):
    admins = GroupPermission.objects.all()
    context = {
        "admins": admins,
    }
    return render(request, "admin/groups/group-permission/admin-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_student_permission(request):
    students = GroupPermission.objects.filter(groupId__slug__contains="ogrenci")
    context = {
        "students": students,
    }
    return render(request, "admin/groups/group-permission/student-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_teacher_permission(request):
    teachers = GroupPermission.objects.filter(groupId__slug__contains="ogretmen")
    context = {
        "teachers": teachers,
    }
    return render(request, "admin/groups/group-permission/teacher-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_moderator_permission(request):
    moderators = GroupPermission.objects.filter(groupId__slug__contains="moderator")
    context = {
        "moderators": moderators,
    }
    return render(request, "admin/groups/group-permission/moderator-permission.html", context)