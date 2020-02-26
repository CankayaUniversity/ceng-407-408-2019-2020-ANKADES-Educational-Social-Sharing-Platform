import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from adminpanel.forms import AdminEditProfileForm, AccountPermissionForm, AccountGroupForm
from account.models import Account, AccountGroup, Permission, Group, AccountPermission
from adminpanel.models import AdminActivity


@login_required(login_url="login_admin")
def admin_all_users(request):
    keyword = request.GET.get("keyword")
    if keyword:
        user_pagination = Account.objects.filter(
            Q(username__contains=keyword) |
            Q(first_name__contains=keyword) |
            Q(last_name__contains=keyword))
        context = {
            "user_pagination": user_pagination,
        }
        return render(request, "admin/account/all-users.html", context)

    accounts = Account.objects.all()
    accountGroups = AccountGroup.objects.all()
    accountFiveLimitOrdered = Account.objects.all().order_by('-date_joined')[:5]
    context = {
        "accounts": accounts,
        "accountGroups": accountGroups,
        "accountFiveLimitOrdered": accountFiveLimitOrdered,
    }
    return render(request, "admin/account/all-users.html", context)


@login_required(login_url="login_admin")
def admin_account_permission(request):
    permissions = AccountPermission.objects.all()
    context = {
        "permissions": permissions,
    }
    return render(request, "admin/account/permission/account-permission.html", context)


@login_required(login_url="login_admin")
def admin_edit_profile(request, username):
    instance = get_object_or_404(Account, username=username)
    form = AdminEditProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.username = username
        instance.save()
        messages.success(request, "Profil başarıyla düzenlendi !")
        return redirect("admin_all_users")
    context = {
        "form": form,
    }
    return render(request, "admin/account/edit-profile.html", context)


@login_required(login_url="login_admin")
def admin_deactivate_profile(request, username):
    instance = get_object_or_404(Account, username=username)
    if instance.is_active is True:
        instance.is_active = False
        activity = AdminActivity()
        activity.activityTitle = "Kullanıcı Etkisizleştirildi."
        activity.activityCreator = request.user.username
        activity.activityMethod = "DELETE"
        activity.activityApplication = "Account"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Kullanıcı artık aktif değil. İşlemi gerçekleştiren kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        activity.save()
        instance.save()
        messages.success(request, "Profil başarıyla etkisizleştirildi.")
        return redirect("admin_all_users")
    messages.error(request, "Kullanıcı zaten aktif değil.")


@login_required(login_url="login_admin")
def admin_blocked_users(request):
    blockedUsers = Account.objects.filter(is_active=False)
    context = {
        "blockedUsers": blockedUsers
    }
    return render(request, "admin/account/blocked-user.html", context)


#Kullanıcı izinleri
@login_required(login_url="login_admin")
def admin_add_account_permission(request):
    form = AccountPermissionForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        form_username = form.cleaned_data.get("userId")
        form_permissionname = form.cleaned_data.get("permissionId")
        if AccountPermission.objects.filter(Q(permissionId=form_permissionname) and Q(userId=form_username)):
            messages.error(request, 'Bu kullanıcıya izin daha önce eklenmiş.')
        else:
            instance = form.save(commit=False)
            activity = AdminActivity()
            activity.activityTitle = "Kullanıcıya izin Ekleme"
            activity.activityCreator = request.user.username
            activity.activityMethod = "POST"
            activity.activityApplication = "Account Permission"
            activity.activityUpdatedDate = datetime.datetime.now()
            activity.activityDescription = "Yeni " + activity.activityApplication + " oluşturuldu. Oluşturan kişi: " + activity.activityCreator
            activity.save()
            instance.save()
            messages.success(request, "Kullanıcıya başarıyla izin eklendi.")
            return redirect("admin_add_account_permission")
    return render(request, "admin/account/permission/add-account-permission.html", context)


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    form = AccountGroupForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        form_username = form.cleaned_data.get("userId")
        form_groupname = form.cleaned_data.get("groupId")
        if AccountGroup.objects.filter(Q(groupId=form_groupname) and Q(userId=form_username)):
            messages.error(request, 'Bu kullanıcıya izin daha önce eklenmiş.')
        else:
            instance = form.save(commit=False)
            activity = AdminActivity()
            activity.activityTitle = "Kullanıcıya Grup Ekleme"
            activity.activityCreator = request.user.username
            activity.activityMethod = "POST"
            activity.activityApplication = "Account Group"
            activity.activityUpdatedDate = datetime.datetime.now()
            activity.activityDescription = "Yeni " + activity.activityApplication + " oluşturuldu. Oluşturan kişi: " + activity.activityCreator
            instance.save()
            activity.save()
            messages.success(request, "Kullanıcıya başarıyla grup eklendi.")
            return redirect("admin_add_account_group")
    return render(request, "admin/account/group/add-account-group.html", context)


@login_required(login_url="login_admin")
def admin_edit_account_group(request, id):
    instance = get_object_or_404(AccountGroup, id=id)
    form = AccountGroupForm(request.POST or None)
    if form.is_valid():
        form_username = form.cleaned_data.get("userId")
        form_groupname = form.cleaned_data.get("groupId")
        if AccountGroup.objects.filter(Q(groupId__slug=form_groupname) and Q(userId__username=form_username)):
            messages.error(request, 'Bu kullanıcıya grup daha önce eklenmiş. Lütfen önce kullanıcının grubunu silin.')
        else:
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            activity = AdminActivity()
            activity.activityTitle = "Kullanıcı Grubu Düzenlendi"
            activity.activityCreator = request.user.username
            activity.activityMethod = "UPDATE"
            activity.activityApplication = "Account Group"
            activity.activityUpdatedDate = datetime.datetime.now()
            activity.activityDescription = "Kullanıcı grubu düzenlendi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
            activity.save()
            instance.save()
            messages.success(request, "Kullanıcı grubu başarıyla güncellendi.")
            return redirect("admin_account_groups")
    return render(request, "admin/account/group/edit-account-group.html", {"form": form})


@login_required(login_url="login_admin")
def admin_edit_account_permission(request, id):
    instance = get_object_or_404(AccountPermission, id=id)
    form = AccountPermissionForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        activity = AdminActivity()
        activity.activityTitle = "Kullanıcı İzni Silindi"
        activity.activityCreator = request.user.username
        activity.activityMethod = "UPDATE"
        activity.activityApplication = "Account Permission"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Kullanıcı izni başarıyla güncellendi. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        instance.save()
        activity.save()
        messages.success(request, "Kullanıcı izni başarıyla düzenlendi !")
        return redirect("admin_account_permission")
    return render(request, "admin/account/permission/edit-account-permission.html", {"form": form})


@login_required(login_url="login_admin")
def admin_deactivate_account_permission(request, id):
    instance = get_object_or_404(AccountPermission, id=id)
    activity = AdminActivity()
    if instance.isActive is False:
        instance.updatedDate = datetime.datetime.now()
        instance.isActive = True
        activity.activityTitle = "Kullanıcı izni etkisizleştirildi"
        activity.activityCreator = request.user.username
        activity.activityMethod = "DELETE"
        activity.activityApplication = "Account Permission"
        activity.activityUpdatedDate = datetime.datetime.utcnow()
        activity.activityDescription = "Kullanıcı izni artık aktif değil. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        activity.save()
        instance.save()
        messages.success(request, "Kullanıcı izni başarıyla etkisizleştirildi.")
        return redirect("admin_account_permission")
    else:
        instance.isActive = False
        instance.updatedDate = datetime.datetime.now()
        activity.activityUpdatedDate = datetime.datetime.utcnow()
        instance.save()
        messages.success(request, "Başarıyla etkisizleştirildi.")
        return redirect("admin_account_permission")


@login_required(login_url="login_admin")
def admin_delete_account_permission(request, id):
    instance = get_object_or_404(AccountPermission, id=id)
    activity = AdminActivity()
    if instance.isActive is False:
        instance.delete()
        activity.activityTitle = "Kullanıcı izni silindi"
        activity.activityCreator = request.user.username
        activity.activityMethod = "DELETE"
        activity.activityApplication = "Account Permission"
        activity.activityUpdatedDate = datetime.datetime.now()
        activity.activityDescription = "Kullanıcı izni artık aktif değil. İşlemi yapan kişi: " + activity.activityCreator + " Uygulama adı: " + activity.activityApplication
        activity.save()
        messages.success(request, "Kullanıcı izni başarıyla silindi.")
        return redirect("admin_account_permission")
    else:
        messages.error(request, "Kullanıcı izni aktif.")
        return redirect("admin_account_permission")
