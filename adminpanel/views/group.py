from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.models import MainGroup, AccountGroup, AccountGroupPermission
from adminpanel.forms import AddAccountMainGroupForm, AddAccountGroupForm, AddAccountGroupPermissionForm


#Gruplar
@login_required(login_url="login_admin")
def admin_all_groups(request):
    groups = MainGroup.objects.all()
    context = {
        "groups": groups,
    }
    return render(request, "admin/groups/groups.html", context)


@login_required(login_url="login_admin")
def admin_add_group(request):
    form = AddAccountMainGroupForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_all_groups")
    context = {
        "form": form,
    }
    return render(request, "admin/groups/add-group.html", context)


@login_required(login_url="login_admin")
def admin_edit_group(request, name_slug):
    instance = get_object_or_404(MainGroup, name_slug=name_slug)
    form = AddAccountMainGroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_all_groups")
    return render(request, "admin/groups/edit-main-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_group(request, name_slug):
    instance = get_object_or_404(MainGroup, name_slug=name_slug)
    instance.delete()
    return redirect("admin_all_groups")


#Grup İzinleri
@login_required(login_url="login_admin")
def admin_add_group_permission(request):
    form = AddAccountGroupPermissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-group-perm.html", context)


@login_required(login_url="login_admin")
def admin_edit_group_permission(request, id):
    instance = get_object_or_404(AccountGroupPermission, id=id)
    form = AddAccountGroupPermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("group_permission")
    return render(request, "admin/groups/edit-group-permission.html", {"form": form})


@login_required(login_url="login_admin")
def admin_group_permission(request):
    group_permissions = AccountGroupPermission.objects.all()
    context = {
        "group_permission": group_permissions,
    }
    return render(request, "admin/groups/group-permissions.html", context)


@login_required(login_url="login_admin")
def admin_delete_group_permission(request, id):
    instance = get_object_or_404(AccountGroupPermission, id=id)
    instance.delete()
    return redirect("group_permission")

#Hesap Grupları
@login_required(login_url="login_admin")
def admin_account_groups(request):
    acc_grp = AccountGroup.objects.all()
    context = {"acc_grp": acc_grp}
    return render(request, "admin/account/group/account-groups.html", context)


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    form = AddAccountGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form_username = form.cleaned_data.get("user_id")
            if AccountGroup.objects.filter(user_id__username=form_username):
                messages.error(request, 'Kullanıcının Grubu Var !')
            else:
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Grup başarıyla kullanıcıya eklendi.')
                return redirect("add_account_group")
        else:
            messages.error(request, 'hata')
    return render(request, "admin/account/group/add-account-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_edit_account_group(request, id):
    instance = get_object_or_404(AccountGroup, id=id)
    form = AddAccountGroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Başarıyle değiştirildi')
        return redirect("edit_account_group")
    return render(request, "admin/account/group/edit-account-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_account_group(request, id):
    instance = get_object_or_404(AccountGroup, id=id)
    instance.delete()
    messages.success(request, 'Başarıyla silindi')
    return redirect("account_groups")