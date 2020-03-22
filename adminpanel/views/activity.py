import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import AccountActivity
from account.views.views import current_user_group
from adminpanel.models import AdminActivity


@login_required(login_url="login_admin")
def admin_all_logs(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    adminLogs = AdminActivity.objects.all()
    accountLogs = AccountActivity.objects.all()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "adminLogs": adminLogs,
        "accountLogs": accountLogs,
    }
    return render(request, "adminpanel/log/all-logs.html", context)


@login_required(login_url="login_admin")
def admin_admin_logs(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    adminLogs = AdminActivity.objects.all()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "adminLogs": adminLogs,
    }
    return render(request, "adminpanel/log/admin-logs.html", context)


@login_required(login_url="login_admin")
def admin_account_logs(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    accountLogs = AccountActivity.objects.all()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "accountLogs": accountLogs,
    }
    return render(request, "adminpanel/log/account-logs.html", context)


@login_required(login_url="login_admin")
def admin_delete_admin_log(request, id):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(AdminActivity, id=id)
    new_activity = AdminActivity()
    new_activity.title = "Admin Log Silme"
    new_activity.creator = currentUser
    new_activity.method = "DELETE"
    new_activity.application = "AdminActivity"
    new_activity.createdDate = datetime.datetime.now()
    if userGroup == 'admin':
        instance.delete()
        new_activity.description = "Admin log silme işlemi başarıyla gerçekleştirildi. Eylemi gerçekleştiren kişi: " + str(currentUser.username)
        new_activity.save()
        messages.success(request, "Admin etkinliği başarıyla silindi")
        return redirect("admin_all_logs")
    else:
        messages.error(request, "Bu eylemi gerçekleştirebilmek için yetkiniz yok.")
        new_activity.description = "Yetkisiz Kullanıcı ! Admin log silme işlemi başarısız. Eylemi gerçekleştiren kişi: " + str(currentUser.username)
        new_activity.save()
        return redirect("admin_all_logs")


@login_required(login_url="login_admin")
def admin_delete_account_log(request, id):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(AccountActivity, id=id)
    new_activity = AdminActivity()
    new_activity.title = "Admin Log Silme"
    new_activity.creator = currentUser
    new_activity.method = "DELETE"
    new_activity.application = "AdminActivity"
    new_activity.createdDate = datetime.datetime.now()
    if userGroup == 'admin':
        instance.delete()
        new_activity.description = "Admin log silme işlemi başarıyla gerçekleştirildi. Eylemi gerçekleştiren kişi: " + str(currentUser.username)
        new_activity.save()
        messages.success(request, "Admin etkinliği başarıyla silindi")
        return redirect("admin_all_logs")
    else:
        messages.error(request, "Bu eylemi gerçekleştirebilmek için yetkiniz yok.")
        new_activity.description = "Yetkisiz Kullanıcı ! Admin log silme işlemi başarısız. Eylemi gerçekleştiren kişi: " + str(currentUser.username)
        new_activity.save()
        return redirect("admin_all_logs")