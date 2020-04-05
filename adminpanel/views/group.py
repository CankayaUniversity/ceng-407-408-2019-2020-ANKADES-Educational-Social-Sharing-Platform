import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import RedirectView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Group
from account.views.views import current_user_group
from adminpanel.forms import AdminEditGroupForm
from adminpanel.models import AdminActivity


@login_required(login_url="login_admin")
def admin_all_groups(request, slug=None):
    """
    :param slug:
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = 'Kullanıcı'
    activity = AdminActivity()
    if request.user.is_authenticated:
        userGroup = current_user_group(request, currentUser)
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
        context = {
            "userGroup": userGroup,
            "groups": groups,
        }
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
    activity = AdminActivity()
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
    activity = AdminActivity()
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
            "userGroup": userGroup
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
    instance = get_object_or_404(Group, slug=slug)
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    activity.title = "Grup Silme"
    activity.method = "DELETE"
    activity.creator = currentUser
    activity.application = "Group"
    activity.createdDate = datetime.datetime.now()
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


# Grup İzinleri
# @login_required(login_url="login_admin")
# def admin_add_group_permission(request):
#     """
#     :param request:
#     :return:
#     """
#     form = AdminGroupPermissionForm(request.POST or None)
#     context = {"form": form, "adminGroup": adminGroup}
#     if form.is_valid():
#         form_groupname = form.cleaned_data.get("groupId")
#         form_permissionname = form.cleaned_data.get("permissionId")
#         if group.isActive is True and permission.isActive is True:
#             if GroupPermission.objects.filter(Q(permissionId=form_permissionname)):
#                 if GroupPermission.objects.filter(Q(groupId=form_groupname)):
#                     messages.error(request, 'Bu gruba izin daha önce eklenmiş.')
#             else:
#                 instance = form.save(commit=False)
#                 activity = AdminActivity()
#                 activity.activityTitle = form.cleaned_data.get("groupId")
#                 activity.activityCreator = request.user.username
#                 activity.activityMethod = "POST"
#                 activity.activityApplication = "Group Permission"
#                 activity.activityUpdatedDate = datetime.datetime.now()
#                 activity.activityDescription = "Yeni " + activity.activityApplication + " oluşturuldu. İşlemi yapan kişi: " + activity.activityCreator
#                 instance.save()
#                 activity.save()
#                 messages.success(request, 'Grup izni başarıyla eklendi.')
#                 return redirect("admin_add_group_permission")
#         else:
#             messages.error(request, "Grup ya da İzin aktif değil. Lütfen kontrol edin.")
#             return redirect("admin_add_group_permission")
#     return render(request, "admin/groups/group-permission/add-group-perm.html", context)
#
#
# @login_required(login_url="login_admin")
# def admin_edit_group_permission(request, id):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     instance = get_object_or_404(GroupPermission, id=id)
#     form = AdminGroupPermissionForm(request.POST or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.updatedDate = datetime.datetime.now()
#         activity = AdminActivity()
#         activity.activityTitle = form.cleaned_data.get("groupId")
#         activity.activityCreator = request.user.username
#         activity.activityMethod = "UPDATE"
#         activity.activityApplication = "Group Permission"
#         activity.activityUpdatedDate = datetime.datetime.now()
#         activity.activityDescription = "Grup izni başarıyla güncellendi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
#         instance.save()
#         activity.save()
#         messages.success(request, "Grup izni başarıyla düzenlendi !")
#         return redirect("admin_group_permission")
#     return render(request, "admin/groups/group-permission/admin-permission.html", {"form": form})
#
#
# @login_required(login_url="login_admin")
# def admin_group_permission(request):
#     """
#     :param request:
#     :return:
#     """
#     groupPermissions = GroupPermission.objects.all()
#     context = {
#         "groupPermissions": groupPermissions,
#     }
#     return render(request, "admin/groups/group-permissions.html", context)
#
#
# @login_required(login_url="login_admin")
# def admin_delete_group_permission(request, id):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     instance = get_object_or_404(GroupPermission, id=id)
#     if instance.isActive is False:
#         activity = AdminActivity()
#         activity.activityTitle = "Grup izni silindi"
#         activity.activityCreator = request.user.username
#         activity.activityMethod = "DELETE"
#         activity.activityApplication = "Group"
#         activity.activityUpdatedDate = datetime.datetime.now()
#         activity.activityDescription = "Grup izni artık aktif değil. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
#         activity.save()
#         instance.save()
#         messages.success(request, "Grup izni başarıyla silindi.")
#     else:
#         messages.error(request, "Grup izni zaten aktif.")
#         return redirect("admin_group_permission")
#     return redirect("admin_group_permission")
#
#
# # Hesap Grupları
# @login_required(login_url="login_admin")
# def admin_account_groups(request):
#     """
#     :param request:
#     :return:
#     """
#     return None
#     # accountGroups = AccountGroup.objects.all()
#     # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     # context = {
#     #     "accountGroups": accountGroups,
#     #     "adminGroup": adminGroup
#     # }
#     # return render(request, "admin/account/group/account-groups.html", context)
#
#
# @login_required(login_url="login_admin")
# def admin_delete_account_group(request, id):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     return None
#     # instance = get_object_or_404(AccountGroup, id=id)
#     # activity = AdminActivity()
#     # activity.activityTitle = "Kullanıcıdan Grup Silindi"
#     # activity.activityCreator = request.user.username
#     # activity.activityMethod = "DELETE"
#     # activity.activityApplication = "Group"
#     # activity.activityUpdatedDate = datetime.datetime.now()
#     # activity.activityDescription = "Silindi. Silen kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
#     # activity.save()
#     # instance.delete()
#     # messages.success(request, 'Başarıyla silindi.')
#     # return redirect("admin_account_groups")
#
#
@login_required(login_url="login_admin")
def admin_isactive_group(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Group, slug=slug)
    getSlug = slug
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    activity.title = "Grup Aktifliği Düzenleme"
    activity.method = "UPDATE"
    activity.creator = currentUser
    activity.application = "Group"
    activity.createdDate = datetime.datetime.now()
    if userGroup == 'admin':
        if instance.isActive:
            instance.updatedDate = datetime.datetime.now()
            instance.isActive = False
            instance.slug = getSlug
            instance.save()
            activity.description = "Grup aktifliği kaldırıldı. İşlemi yapan kişi: " + str(
                activity.creator) + ". İşleminin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.success(request, "Group artık aktif değil.")
            return redirect("admin_all_groups")
        else:
            instance.isActive = True
            instance.updatedDate = datetime.datetime.now()
            instance.slug = slug
            instance.save()
            activity.description = "Grup başarıyla aktifleştirildi. İşlemi yapan kişi: " + str(
                activity.creator) + ". İşleminin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.success(request, "Group aktifleştirildi.")
            return redirect("admin_all_groups")
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_all_groups")
