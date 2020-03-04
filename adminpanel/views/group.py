from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
import datetime
from rest_framework import request
from rest_framework.generics import get_object_or_404
from account.models import AccountGroup, Group, GroupPermission, Permission, Account
from adminpanel.forms import AdminGroupForm, AdminGroupPermissionForm
from adminpanel.models import AdminActivity


user = Account()
group = Group()
permission = Permission()
groupPermission = GroupPermission()
userGroup = AccountGroup()


@login_required(login_url="login_admin")
def admin_all_groups(request):
    """
    :param request:
    :return:
    """
    groups = Group.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "groups": groups,
        "adminGroup": adminGroup,
    }
    return render(request, "admin/groups/groups.html", context)


@login_required(login_url="login_admin")
def admin_add_group(request):
    """
    :param request:
    :return:
    """
    form = AdminGroupForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
            # accountGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
            # if accountGroup:
            instance = form.save(commit=False)
            activity = AdminActivity()
            activity.activityTitle = form.cleaned_data.get("title")
            activity.activityCreator = request.user.username
            activity.activityMethod = "POST"
            activity.activityApplication = "Group"
            activity.activityUpdatedDate = datetime.datetime.now()
            activity.activityDescription = "Yeni " + activity.activityApplication + " oluşturuldu. İşlemi yapan kişi: " + activity.activityCreator
            instance.save()
            activity.save()
            messages.success(request, "Grup başarıyla eklendi !")
            return redirect("admin_add_group")
        return render(request, "admin/groups/add-group.html", {"form": form, "adminGroup": adminGroup})
    else:
        messages.error(request, "Yetkiniz Yok !")
        return redirect("admin_index")



@login_required(login_url="login_admin")
def admin_edit_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    form = AdminGroupForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        activity = AdminActivity()
        activity.activityTitle = "Group Güncellendi."
        activity.activityCreator = request.user.username
        activity.activityMethod = "UPDATE"
        activity.activityApplication = "Group"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Güncellendi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        instance.save()
        activity.save()
        messages.success(request, "Grup başarıyla düzenlendi.")
        return redirect("admin_all_groups")
    return render(request, "admin/groups/edit-main-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    instance.delete()
    activity = AdminActivity()
    activity.activityTitle = "Grup Silindi"
    activity.activityCreator = request.user.username
    activity.activityMethod = "DELETE"
    activity.activityApplication = "Group"
    activity.activityUpdatedDate = datetime.datetime.now()
    activity.activityDescription = "Grup silindi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
    activity.save()
    instance.save()
    messages.success(request, "Grup başarıyla silindi.")
    return redirect("admin_all_groups")


# Grup İzinleri
@login_required(login_url="login_admin")
def admin_add_group_permission(request):
    """
    :param request:
    :return:
    """
    form = AdminGroupPermissionForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {"form": form, "adminGroup": adminGroup}
    if adminGroup:
        if form.is_valid():
            form_groupname = form.cleaned_data.get("groupId")
            form_permissionname = form.cleaned_data.get("permissionId")
            if group.isActive is True and permission.isActive is True:
                if GroupPermission.objects.filter(Q(permissionId=form_permissionname)):
                    if GroupPermission.objects.filter(Q(groupId=form_groupname)):
                        messages.error(request, 'Bu gruba izin daha önce eklenmiş.')
                else:
                    instance = form.save(commit=False)
                    activity = AdminActivity()
                    activity.activityTitle = form.cleaned_data.get("groupId")
                    activity.activityCreator = request.user.username
                    activity.activityMethod = "POST"
                    activity.activityApplication = "Group Permission"
                    activity.activityUpdatedDate = datetime.datetime.now()
                    activity.activityDescription = "Yeni " + activity.activityApplication + " oluşturuldu. İşlemi yapan kişi: " + activity.activityCreator
                    instance.save()
                    activity.save()
                    messages.success(request, 'Grup izni başarıyla eklendi.')
                    return redirect("admin_add_group_permission")
            else:
                messages.error(request, "Grup ya da İzin aktif değil. Lütfen kontrol edin.")
                return redirect("admin_add_group_permission")
        return render(request, "admin/groups/group-permission/add-group-perm.html", context)
    else:
        messages.error(request, "Yetkiniz Yok !")


@login_required(login_url="login_admin")
def admin_edit_group_permission(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(GroupPermission, id=id)
    form = AdminGroupPermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        activity = AdminActivity()
        activity.activityTitle = form.cleaned_data.get("groupId")
        activity.activityCreator = request.user.username
        activity.activityMethod = "UPDATE"
        activity.activityApplication = "Group Permission"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Grup izni başarıyla güncellendi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        instance.save()
        activity.save()
        messages.success(request, "Grup izni başarıyla düzenlendi !")
        return redirect("admin_group_permission")
    return render(request, "admin/groups/group-permission/admin-permission.html", {"form": form})


@login_required(login_url="login_admin")
def admin_group_permission(request):
    """
    :param request:
    :return:
    """
    groupPermissions = GroupPermission.objects.all()
    context = {
        "groupPermissions": groupPermissions,
    }
    return render(request, "admin/groups/group-permissions.html", context)


@login_required(login_url="login_admin")
def admin_delete_group_permission(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(GroupPermission, id=id)
    if instance.isActive is False:
        activity = AdminActivity()
        activity.activityTitle = "Grup izni silindi"
        activity.activityCreator = request.user.username
        activity.activityMethod = "DELETE"
        activity.activityApplication = "Group"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Grup izni artık aktif değil. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        activity.save()
        instance.save()
        messages.success(request, "Grup izni başarıyla silindi.")
    else:
        messages.error(request, "Grup izni zaten aktif.")
        return redirect("admin_group_permission")
    return redirect("admin_group_permission")


@login_required(login_url="login_admin")
def admin_deactivate_group_permission(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(GroupPermission, id=id)
    activity = AdminActivity()
    if instance.isActive is True:
        instance.isActive = False
        instance.updatedDate = datetime.datetime.utcnow()
        activity.activityTitle = "Grup izni etkisizleştirildi"
        activity.activityCreator = request.user.username
        activity.activityMethod = "DELETE"
        activity.activityApplication = "Group"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Grup izni artık aktif değil. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        instance.save()
        activity.save()
        messages.success(request, "Grup izni başarıyla etkisizleştirildi.")
    else:
        instance.isActive = True
        instance.updatedDate = datetime.datetime.now()
        activity.activityUpdatedDate = datetime.datetime.utcnow()
        instance.save()
        activity.save()
        messages.error(request, "Grup izni aktifleştirildi.")
    return redirect("admin_group_permission")


# Hesap Grupları
@login_required(login_url="login_admin")
def admin_account_groups(request):
    """
    :param request:
    :return:
    """
    accountGroups = AccountGroup.objects.all()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "accountGroups": accountGroups,
        "adminGroup": adminGroup
    }
    return render(request, "admin/account/group/account-groups.html", context)


@login_required(login_url="login_admin")
def admin_deactivate_account_group(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(AccountGroup, id=id)
    activity = AdminActivity()
    if instance.isActive is True:
        instance.updatedDate = datetime.datetime.utcnow()
        instance.isActive = False
        activity.activityTitle = "Kullanıcı Grubu Etkinleştirildi."
        activity.activityCreator = request.user.username
        activity.activityMethod = "UPDATE"
        activity.activityApplication = "Account Group"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Kullanıcı grubu etkinleştirildi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        instance.save()
        activity.save()
        messages.success(request, 'Başarıyla etkinleştirildi.')
        return redirect("admin_account_groups")
    else:
        instance.isActive = True
        instance.updatedDate = datetime.datetime.utcnow()
        instance.save()
        activity.updatedDate = datetime.datetime.utcnow()
        activity.save()
        messages.success(request, "Hesabın grubu başarıyla etkisizleştirildi")
        return redirect("admin_account_groups")


@login_required(login_url="login_admin")
def admin_delete_account_group(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(AccountGroup, id=id)
    activity = AdminActivity()
    activity.activityTitle = "Kullanıcıdan Grup Silindi"
    activity.activityCreator = request.user.username
    activity.activityMethod = "DELETE"
    activity.activityApplication = "Group"
    activity.activityUpdatedDate = datetime.datetime.now()
    activity.activityDescription = "Silindi. Silen kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
    activity.save()
    instance.delete()
    messages.success(request, 'Başarıyla silindi.')
    return redirect("admin_account_groups")


@login_required(login_url="login_admin")
def admin_activation_edit_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    activity = AdminActivity()
    if instance.isActive is False:
        instance.updatedDate = datetime.datetime.now()
        instance.isActive = True
        activity.activityTitle = "Group etkinleştirildi"
        activity.activityCreator = request.user.username
        activity.activityMethod = "UPDATE"
        activity.activityApplication = "Group"
        activity.activityUpdatedDate = datetime.datetime.utcnow()
        activity.activityDescription = "Grup etkinleştirildi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        activity.save()
        instance.save()
        messages.success(request, "Group etkinleştirildi.")
        return redirect("admin_all_groups")
    else:
        instance.isActive = False
        instance.updatedDate = datetime.datetime.now()
        activity.activityUpdatedDate = datetime.datetime.utcnow()
        instance.save()
        activity.save()
        messages.success(request, "Başarıyla etkisizleştirildi.")
        return redirect("admin_all_groups")