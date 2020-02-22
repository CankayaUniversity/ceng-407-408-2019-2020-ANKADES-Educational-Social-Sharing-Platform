from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.models import AccountGroupPermission, MainPermission
from adminpanel.forms import AddAccountMainPermissionForm, AddAccountGroupPermissionForm


#İzinler
@login_required(login_url="login_admin")
def admin_all_permissions(request):
    permissions = MainPermission.objects.all()
    context = {
        "permissions": permissions,
    }
    return render(request, "admin/permissions/all-permissions.html", context)


@login_required(login_url="login_admin")
def admin_add_permission(request):
    form = AddAccountMainPermissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-permission.html", context)


@login_required(login_url="login_admin")
def admin_delete_permission(request, name_slug):
    instance = get_object_or_404(MainPermission, name_slug=name_slug)
    instance.delete()
    return redirect("all_permissions")


@login_required(login_url="login_admin")
def admin_edit_permission(request, name_slug):
    instance = get_object_or_404(MainPermission, name_slug=name_slug)
    form = AddAccountMainPermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("all_permissions")
    return render(request, "admin/permissions/edit-main-permission.html", {"form": form})


#Grup İzinleri
@login_required(login_url="login_admin")
def admin_site_admin_permission(request):
    admin = AccountGroupPermission.objects.filter(group_id__name_slug__contains="admin")
    context = {
        "admin": admin,
    }
    return render(request, "admin/groups/group-permission/admin-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_student_permission(request):
    student = AccountGroupPermission.objects.filter(group_id__name_slug__contains="ogrenci")
    context = {
        "student": student,
    }
    return render(request, "admin/groups/group-permission/student-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_teacher_permission(request):
    teacher = AccountGroupPermission.objects.filter(group_id__name_slug__contains="ogretmen")
    context = {
        "teacher": teacher,
    }
    return render(request, "admin/groups/group-permission/teacher-permission.html", context)


@login_required(login_url="login_admin")
def admin_site_moderator_permission(request):
    moderator = AccountGroupPermission.objects.filter(group_id__name_slug__contains="moderator")
    context = {
        "moderator": moderator,
    }
    return render(request, "admin/groups/group-permission/moderator-permission.html", context)