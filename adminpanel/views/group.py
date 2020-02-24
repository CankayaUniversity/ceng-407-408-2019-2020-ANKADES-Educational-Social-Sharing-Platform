from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from account.models import AccountGroup, Group, GroupPermission
from adminpanel.forms import GroupForm, GroupPermissionForm, AccountGroupForm


@login_required(login_url="login_admin")
def admin_all_groups(request):
    groups = Group.objects.all()
    context = {
        "groups": groups,
    }
    return render(request, "admin/groups/groups.html", context)


@login_required(login_url="login_admin")
def admin_add_group(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Grup başarıyla eklendi !")
        return redirect("admin_all_groups")
    context = {
        "form": form,
    }
    return render(request, "admin/groups/add-group.html", context)


@login_required(login_url="login_admin")
def admin_edit_group(request, name_slug):
    instance = get_object_or_404(Group, name_slug=name_slug)
    form = GroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Grup başarıyla düzenlendi !")
        return redirect("admin_all_groups")
    return render(request, "admin/groups/edit-main-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_group(request, name_slug):
    instance = get_object_or_404(Group, name_slug=name_slug)
    instance.delete()
    success = True
    if success is True:
        messages.success(request, "Grup başarıyla silindi !")
    else:
        messages.error(request, "Grup silinirken bir sorun oluştu. Lütfen daha sonra tekrar deneyin.")
    return redirect("admin_all_groups")


# Grup İzinleri
@login_required(login_url="login_admin")
def admin_add_group_permission(request):
    form = GroupPermissionForm(request.POST or None)
    if form.is_valid():
        form_groupname = form.cleaned_data.get("groupId")
        form_permissionname = form.cleaned_data.get("permissionId")
        if GroupPermission.objects.filter(Q(permissionId=form_permissionname) and Q(groupId=form_groupname)):
            messages.error(request, 'Bu gruba izin daha önce eklenmiş !')
        else:
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Grup izni başarıyla kullanıcıya eklendi.')
            return redirect("admin_add_group_permission")

        return redirect("admin_add_group_permission")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-group-perm.html", context)


@login_required(login_url="login_admin")
def admin_edit_group_permission(request, id):
    instance = get_object_or_404(GroupPermission, id=id)
    form = GroupPermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Grup izni başarıyla düzenlendi !")
        return redirect("admin_group_permission")
    return render(request, "admin/groups/edit-group-permission.html", {"form": form})


@login_required(login_url="login_admin")
def admin_group_permission(request):
    group_permissions = GroupPermission.objects.all()
    context = {
        "group_permission": group_permissions,
    }
    return render(request, "admin/groups/group-permissions.html", context)


@login_required(login_url="login_admin")
def admin_delete_group_permission(request, id):
    instance = get_object_or_404(GroupPermission, id=id)
    instance.delete()
    success = True
    if success is True:
        messages.success(request, "Grup izni başarıyla silindi !")
    else:
        messages.error(request, "Grup izni silinirken bir sorun oluştu. Lütfen tekrar deneyin")
    return redirect("admin_group_permission")


# Hesap Grupları
@login_required(login_url="login_admin")
def admin_account_groups(request):
    acc_grp = AccountGroup.objects.all()
    context = {"acc_grp": acc_grp}
    return render(request, "admin/account/group/account-groups.html", context)


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    form = AccountGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form_username = form.cleaned_data.get("userId")
            if AccountGroup.objects.filter(Q(userId__username=form_username)):
                messages.error(request, 'Kullanıcının Grubu Var !')
            else:
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Grup başarıyla kullanıcıya eklendi.')
                return redirect("admin_add_account_group")
        else:
            messages.error(request, 'hata')
    return render(request, "admin/account/group/add-account-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_edit_account_group(request, id):
    instance = get_object_or_404(AccountGroup, id=id)
    form = AccountGroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        success = True
        if success is True:
            messages.success(request, 'Başarıyle değiştirildi')
        else:
            messages.error(request, "hata")
        return redirect("admin_edit_account_group")
    return render(request, "admin/account/group/edit-account-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_account_group(request, id):
    instance = get_object_or_404(AccountGroup, id=id)
    instance.delete()
    messages.success(request, 'Başarıyla silindi')
    return redirect("admin_account_groups")
