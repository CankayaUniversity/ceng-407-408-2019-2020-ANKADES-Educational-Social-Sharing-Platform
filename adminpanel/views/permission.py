import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from account.models import GroupPermission, Permission
from account.views.views import current_user_group
from adminpanel.forms import AdminPermissionForm
from adminpanel.models import AdminActivity


@login_required(login_url="login_admin")
def admin_all_permissions(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    permissions = Permission.objects.all()
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "permissions": permissions,
    }
    return render(request, "admin/permissions/all-permissions.html", context)


@login_required(login_url="login_admin")
def admin_add_permission(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    activity.application = "Permission"
    activity.creator = currentUser
    activity.title = "İzin Ekle"
    activity.method = "POST"
    activity.createdDate = datetime.datetime.now()
    if userGroup == 'admin':
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            isActive = request.POST.get("isActive") == 'on'
            new_group = Permission(title=title, description=description, isActive=isActive)
            new_group.save()
            activity.description = "Yeni bir izin eklendi. İşlemi yapan kişi: " + str(activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate) + ""
            activity.save()
            messages.success(request, "İzin başarıyla oluşturuldu.")
            return redirect("admin_all_permissions")
        context = {
            "currentUser": currentUser,
            "userGroup": userGroup,
        }
        return render(request, "adminpanel/permission/add-permission.html", context)
    else:
        activity.description = "Yeni bir grup ekleme başarısız. İşlemi yapan kişi: " + str(
            activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate)
        activity.save()
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")
#
#
# @login_required(login_url="login_admin")
# def admin_delete_permission(request, slug):
#     """
#     :param request:
#     :param slug:
#     :return:
#     """
#     return None
#     # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     # if adminGroup:
#     #     instance = get_object_or_404(Permission, slug=slug)
#     #     instance.isActive = False
#     #     messages.success(request, "İzin başarıyla silindi.")
#     #     return redirect("admin_all_permissions")
#     # else:
#     #     messages.error(request, "Yetkiniz yok !")
#     #     return redirect("admin_dashboard")
#
#
# @login_required(login_url="login_admin")
# def admin_edit_permission(request, slug):
#     """
#     :param request:
#     :param slug:
#     :return:
#     """
#     # adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     # if adminGroup:
#     #     instance = get_object_or_404(Permission, slug=slug)
#     #     form = AdminPermissionForm(request.POST or None, instance=instance)
#     #     if form.is_valid():
#     #         instance = form.save(commit=False)
#     #         instance.updatedDate = datetime.datetime.now()
#     #         instance.save()
#     #         messages.success(request, "İzin başarıyla güncellendi.")
#     #         return redirect("admin_all_permissions")
#     #     return render(request, "admin/permissions/edit-main-permission.html", {"form": form})
#     # else:
#     #     messages.error(request, "Yetkiniz yok !")
#     #     return redirect("admin_dashboard")
#     return None
#
#
# #Grup İzinleri
# @login_required(login_url="login_admin")
# def admin_site_admin_permission(request):
#     """
#     :param request:
#     :return:
#     """
#     admins = GroupPermission.objects.all()
#     context = {
#         "admins": admins,
#     }
#     return render(request, "admin/groups/group-permission/admin-permission.html", context)
#
#
# @login_required(login_url="login_admin")
# def admin_site_student_permission(request):
#     """
#     :param request:
#     :return:
#     """
#     students = GroupPermission.objects.filter(groupId__slug__contains="ogrenci")
#     context = {
#         "students": students,
#     }
#     return render(request, "admin/groups/group-permission/student-permission.html", context)
#
#
# @login_required(login_url="login_admin")
# def admin_site_teacher_permission(request):
#     """
#     :param request:
#     :return:
#     """
#     teachers = GroupPermission.objects.filter(groupId__slug__contains="ogretmen")
#     context = {
#         "teachers": teachers,
#     }
#     return render(request, "admin/groups/group-permission/teacher-permission.html", context)
#
#
# @login_required(login_url="login_admin")
# def admin_site_moderator_permission(request):
#     """
#     :param request:
#     :return:
#     """
#     moderators = GroupPermission.objects.filter(groupId__slug__contains="moderator")
#     context = {
#         "moderators": moderators,
#     }
#     return render(request, "admin/groups/group-permission/moderator-permission.html", context)