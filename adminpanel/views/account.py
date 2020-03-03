import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from account.forms import AccountRegisterForm
from account.models import Account, AccountGroup, Group, AccountPermission
from adminpanel.forms import AdminEditProfileForm, AdminAccountPermissionForm, AdminAccountGroupForm
from adminpanel.models import AdminActivity

user = Account()
group = Group()


@login_required(login_url="login_admin")
def admin_all_users(request):
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
def admin_students(request):
    accounts = AccountGroup.objects.filter(Q(groupId__slug="ogrenci"))
    context = {
        "accounts": accounts,
    }
    return render(request, "admin/account/group/students.html", context)


@login_required(login_url="login_admin")
def admin_teachers(request):
    accounts = AccountGroup.objects.filter(Q(groupId__slug="ogretmen"))
    context = {
        "accounts": accounts,
    }
    return render(request, "admin/account/group/teachers.html", context)


@login_required(login_url="login_admin")
def admin_moderators(request):
    accounts = AccountGroup.objects.filter(Q(groupId__slug="moderator"))
    context = {
        "accounts": accounts,
    }
    return render(request, "admin/account/group/moderators.html", context)


@login_required(login_url="login_admin")
def admin_admins(request):
    accounts = AccountGroup.objects.filter(Q(groupId__slug="admin"))
    context = {
        "accounts": accounts,
    }
    return render(request, "admin/account/group/admins.html", context)


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
    accountGroup = AccountGroup.objects.filter(
        Q(userId__username=request.user.username, groupId__slug="moderator") | Q(
            userId__username=request.user.username, groupId__slug="admin"))
    if form.is_valid():
        if accountGroup:
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.username = username
            instance.save()
            messages.success(request, "Profil başarıyla düzenlendi !")
            return redirect("admin_all_users")
        else:
            messages.error(request, "Yetkiniz Yok")
    context = {
        "form": form,
        "accountGroup": accountGroup
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


# Kullanıcı izinleri
@login_required(login_url="login_admin")
def admin_add_account_permission(request):
    form = AdminAccountPermissionForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "form": form,
        "adminGroup": adminGroup,
    }
    if adminGroup:
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
    else:
        messages.error(request, "Yetkiniz yok !")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    """
    :param request:
    :return:
    """
    form = AdminAccountGroupForm(request.POST or None)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {"form": form, "adminGroup": adminGroup}
    if adminGroup:
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
                activity.activityDescription = "Yeni " + activity.activityApplication + " oluşturuldu. İşlem yapılan kullanıcı: x. İşlemi yapan kişi: " + activity.activityCreator
                instance.save()
                activity.save()
                messages.success(request, "Kullanıcıya başarıyla grup eklendi.")
                return redirect("admin_add_account_group")
        return render(request, "admin/account/group/add-account-group.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_edit_account_group(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(AccountGroup, id=id)
    form = AdminAccountGroupForm(request.POST or None, instance=instance)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
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
        return render(request, "admin/account/group/edit-account-group.html", {"form": form, "adminGroup": adminGroup})
    else:
        messages.error(request, "Yetkiniz Yok !")


@login_required(login_url="login_admin")
def admin_edit_account_permission(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(AccountPermission, id=id)
    form = AdminAccountPermissionForm(request.POST or None, instance=instance)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
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
        return render(request, "admin/account/permission/edit-account-permission.html", {"form": form, "adminGroup": adminGroup})
    else:
        messages.error(request, "Yetkiniz Yok!")


@login_required(login_url="login_admin")
def admin_deactivate_account_permission(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(AccountPermission, id=id)
    activity = AdminActivity()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
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
    else:
        messages.error(request, "Yetkiniz Yok!")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_delete_account_permission(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    instance = get_object_or_404(AccountPermission, id=id)
    activity = AdminActivity()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
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
    else:
        messages.error(request, "Yetkiniz Yok!")


@login_required(login_url="login_admin")
def admin_register_account(request):
    form = AccountRegisterForm(request.POST or None)
    getGroup = Group.objects.get(slug="ogrenci")
    accountGroup = AccountGroup()
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            new_user = Account(username=username, email=email)
            new_user.is_active = True
            new_user.is_admin = False
            new_user.save()
            new_user.set_password(password)
            new_user.save()
            accountGroup.userId_id = new_user.id
            accountGroup.groupId_id = getGroup.id
            accountGroup.save()
            messages.success(request, "Kayıt işlemi başarıyla gerçekleştirildi.")
            return redirect("admin_account_settings")
        context = {
            "form": form,
            "adminGroup": adminGroup
        }
        return render(request, "admin/settings/add-account.html", context)
    else:
        messages.error(request, "Yetkiniz Yok !")
