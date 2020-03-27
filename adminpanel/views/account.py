import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.forms import AccountRegisterForm
from account.models import Account, Group, AccountGroup
from account.views.views import current_user_group
from adminpanel.forms import AdminEditProfileForm
from adminpanel.models import AdminActivity
from exam.models import School


@login_required(login_url="login_admin")
def admin_all_users(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    accounts = Account.objects.all().order_by('-date_joined')[:5]
    context = {
        "userGroup": userGroup,
        "accounts": accounts,
    }
    return render(request, "adminpanel/account/all-users.html", context)


@login_required(login_url="login_admin")
def admin_all_user_groups(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)

    admins = AccountGroup.objects.filter(Q(groupId__slug="admin"))
    moderators = AccountGroup.objects.filter(Q(groupId__slug="moderator"))
    teachers = AccountGroup.objects.filter(Q(groupId__slug="ogretmen"))
    students = AccountGroup.objects.filter(Q(groupId__slug="ogrenci"))
    members = AccountGroup.objects.filter(Q(groupId__slug="üye"))
    accounts = Account.objects.all().order_by('-date_joined')[:5]
    context = {
        "userGroup": userGroup,
        "admins": admins,
        "moderators": moderators,
        "teachers": teachers,
        "students": students,
    }
    return render(request, "adminpanel/account/group/user-groups.html", context)


@login_required(login_url="login_admin")
def admin_my_account(request, username):
    currentUser = request.user
    userDetail = get_object_or_404(Account, username=username)
    userGroup = current_user_group(request, currentUser)
    context = {
        "userDetail": userDetail,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/my-profile.html", context)


@login_required(login_url="login_admin")
def admin_students(request):
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    students = AccountGroup.objects.filter(Q(groupId__slug="ogrenci"))
    context = {
        "students": students,
        "adminGroup": adminGroup,
    }
    return render(request, "adminpanel/account/group/students.html", context)


@login_required(login_url="login_admin")
def admin_teachers(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    teachers = AccountGroup.objects.filter(Q(groupId__slug="ogretmen"))
    context = {
        "teachers": teachers,
        "userGroup": userGroup,
        "currentUser": currentUser,
    }
    return render(request, "adminpanel/account/group/teachers.html", context)


@login_required(login_url="login_admin")
def admin_moderators(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    moderators = AccountGroup.objects.filter(Q(groupId__slug="moderator"))
    context = {
        "moderators": moderators,
        "userGroup": userGroup,
        "currentUser": currentUser,
    }
    return render(request, "adminpanel/account/group/moderators.html", context)


@login_required(login_url="login_admin")
def admin_members(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    members = AccountGroup.objects.filter(Q(groupId__slug="member"))
    context = {
        "members": members,
        "userGroup": userGroup,
        "currentUser": currentUser,
    }
    return render(request, "adminpanel/account/group/members.html", context)


@login_required(login_url="login_admin")
def admin_admins(request):
    admins = AccountGroup.objects.filter(groupId__slug="admin")
    moderators = AccountGroup.objects.filter(groupId__slug="moderator")
    teachers = AccountGroup.objects.filter(groupId__slug="ogretmen")
    students = AccountGroup.objects.filter(groupId__slug="ogrenci")
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "admins": admins,
        "moderators": moderators,
        "teachers": teachers,
        "students": students,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/group/admins.html", context)


@login_required(login_url="login_admin")
def admin_edit_profile(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    schools = School.objects.filter(Q(isActive=False, isCategory=False))
    activity = AdminActivity()
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        instance.first_name = first_name
        instance.last_name = last_name
        instance.username = username
        instance.save()
        activity.title = "Profil Güncelleme"
        activity.application = "Account"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(activity.creator) + " kullanıcısı hesabını güncelledi."
        activity.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect(reverse("admin_edit_profile", kwargs={"username": username}))
    context = {
        "instance": instance,
        "currentUser": currentUser,
        "userGroup": userGroup,
        "schools": schools,
    }
    return render(request, "adminpanel/account/edit-profile.html", context)


@login_required(login_url="login_admin")
def admin_edit_username(request, username):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=username)
    activity = AdminActivity()
    context = {
        "userGroup": userGroup,
        "instance": instance
    }
    if request.method == "POST":
        username = request.POST.get('username')
        instance = Account(username=username)
        instance.save()
        activity.title = "Profil Güncelleme"
        activity.application = "Account"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı kullanıcı adını güncelledi."
        activity.save()
        messages.success(request, "Kullanıcı adınız başarıyla güncellendi.")
        return redirect("admin_edit_username")
    return render(request, "adminpanel/account/edit-username.html", context)


@login_required(login_url="login_admin")
def admin_edit_email(request, username):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=username)
    activity = AdminActivity()
    context = {
        "userGroup": userGroup,
        "instance": instance
    }
    if request.method == "POST":
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm_email')
        context = {
            "email": email,
            "confirm_email": confirm_email,
            "userGroup": userGroup,
            "instance": instance
        }
        if email != confirm_email:
            messages.error(request, "E-mail adresleri uyuşmuyor. Lütfen tekrar deneyin")
            return render(request, "adminpanel/account/edit-email.html", context)
        else:
            instance = Account(email=email)
            instance.save()
            activity.title = "E-mail Güncelleme: " + str(currentUser)
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = currentUser
            activity.description = str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı e-mail adresini güncelledi."
            activity.save()
            messages.success(request, "Email adresiniz başarıyla güncellendi.")
            return redirect("admin_edit_profile")
    return render(request, "adminpanel/account/edit-email.html", context)


@login_required(login_url="login_admin")
def admin_blocked_users(request):
    activity = AdminActivity()
    blockedUsers = Account.objects.filter(is_active=False)
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    context = {
        "users": blockedUsers,
        "userGroup": userGroup,
    }
    if userGroup == 'admin':
        return render(request, "adminpanel/account/blocked-user.html", context)
    else:
        activity.title = "Giriş Yapma"
        activity.application = "Account"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısının yetkisi yok."
        activity.save()
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_block_account(request, username):
    user = get_object_or_404(Account, username=username)
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    if userGroup == 'admin' or userGroup == 'moderator':
        if user.is_active is True:
            user.is_active = False
            user.save()
            activity.title = "Kullanıcı Engelleme"
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = currentUser
            activity.description = str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı engellendi."
            activity.save()
            messages.success(request, "Kullanıcı başarıyla engellendi.")
            return redirect("admin_all_users")
        else:
            user.is_active = True
            user.save()
            activity.title = "Kullanıcı Aktifleştirme"
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = currentUser
            activity.description = str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı aktifleştirildi."
            activity.save()
            messages.success(request, "Kullanıcı başarıyla aktifleştirildi.")
            return redirect("admin_all_users")
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_all_users")


@login_required(login_url="login_admin")
def admin_register_account(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    getGroup = Group.objects.get(slug="uye")
    accountGroup = AccountGroup()
    activity = AdminActivity()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser
    }
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_active = request.POST.get('is_active') == "on"
        if password and confirm_password and password != confirm_password:
            messages.error(request, "Girilen şifreler uyuşmuyor. Lütfen tekrar deneyin.")
            return render(request, "adminpanel/account/add-account.html", context)
        else:
            new_user = Account(first_name=first_name, last_name=last_name, username=username, email=email, is_active=is_active)
            new_user.is_admin = False
            new_user.is_staff = False
            new_user.save()
            new_user.set_password(password)
            new_user.save()
            accountGroup.userId_id = new_user.id
            accountGroup.groupId_id = getGroup.id
            accountGroup.save()
            activity.title = "Kullanıcı Ekleme"
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = currentUser
            activity.description = str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı eklendi."
            activity.save()
            messages.success(request, "Yeni kullanıcı başarıyla eklendi.")
            return redirect("admin_all_users")
    return render(request, "adminpanel/account/add-account.html", context)

# # Kullanıcı izinleri
# @login_required(login_url="login_admin")
# def admin_add_account_permission(request):
#     form = AdminAccountPermissionForm(request.POST or None)
#     adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     context = {
#         "form": form,
#         "adminGroup": adminGroup,
#     }
#     if adminGroup:
#         if form.is_valid():
#             userId = form.cleaned_data.get("userId")
#             permissionId = form.cleaned_data.get("permissionId")
#             isActive = form.cleaned_data.get("isActive")
#             if AccountPermission.objects.filter(Q(permissionId=permissionId, userId=userId)):
#                 messages.error(request, 'Bu kullanıcıya izin daha önce eklenmiş.')
#             else:
#                 instance = AccountPermission(userId=userId, permissionId=permissionId, isActive=isActive)
#                 activity = AdminActivity()
#                 activity.title = "Kullanıcıya izin ekleme"
#                 activity.creator = request.user.username
#                 activity.method = "POST"
#                 activity.application = "Account Permission"
#                 activity.updatedDate = datetime.datetime.now()
#                 activity.description = "Yeni " + activity.application + " oluşturuldu. Oluşturan kişi: " + activity.creator
#                 activity.save()
#                 instance.save()
#                 messages.success(request, "Kullanıcıya başarıyla izin eklendi.")
#                 return redirect("admin_add_account_permission")
#         return render(request, "admin/account/permission/add-account-permission.html", context)
#     else:
#         messages.error(request, "Yetkiniz yok !")
#         return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_add_account_group(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    if request.method == "POST":
        group = request.POST['groupId']
        user = request.POST['userId']
        instance = AccountGroup(userId=user, groupId=group)

    return None


# @login_required(login_url="login_admin")
# def admin_edit_account_group(request, id):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     instance = get_object_or_404(AccountGroup, id=id)
#     form = AdminAccountGroupForm(request.POST or None, instance=instance)
#     adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     if adminGroup:
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.updatedDate = datetime.datetime.now()
#             activity = AdminActivity()
#             activity.title = "Kullanıcı grubu düzenlendi"
#             activity.creator = request.user.username
#             activity.method = "UPDATE"
#             activity.application = "Account Group"
#             activity.updatedDate = datetime.datetime.now()
#             activity.description = "Kullanıcı grubu düzenlendi. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#             activity.save()
#             instance.save()
#             messages.success(request, "Kullanıcı grubu başarıyla güncellendi.")
#             return redirect("admin_account_groups")
#         return render(request, "admin/account/group/edit-account-group.html", {"form": form, "adminGroup": adminGroup})
#     else:
#         messages.error(request, "Yetkiniz Yok !")
#
#
# @login_required(login_url="login_admin")
# def admin_edit_account_permission(request, id):
#     """
#     :param request:
#     :param id:
#     :return:
#     """
#     instance = get_object_or_404(AccountPermission, id=id)
#     form = AdminAccountPermissionForm(request.POST or None, instance=instance)
#     adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     if adminGroup:
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.updatedDate = datetime.datetime.now()
#             activity = AdminActivity()
#             activity.title = "Kullanıcı izni silindi"
#             activity.creator = request.user.username
#             activity.me = "UPDATE"
#             activity.application = "Account Permission"
#             activity.updatedDate = datetime.datetime.now()
#             activity.description = "Kullanıcı izni başarıyla güncellendi. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#             activity.save()
#             instance.save()
#             messages.success(request, "Kullanıcı izni başarıyla düzenlendi !")
#             return redirect("admin_account_permission")
#         return render(request, "admin/account/permission/edit-account-permission.html", {"form": form, "adminGroup": adminGroup})
#     else:
#         messages.error(request, "Yetkiniz Yok!")
#
#
# @login_required(login_url="login_admin")
# def admin_deactivate_account_permission(request, id):
#     """
#     :param request:ku
#     :param id:
#     :return:
#     """
#     instance = get_object_or_404(AccountPermission, id=id)
#     activity = AdminActivity()
#     adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
#     if adminGroup:
#         if instance.isActive is True:
#             instance.isActive = False
#             activity.title = "Kullanıcı izni etkisizleştirildi"
#             activity.creator = request.user.username
#             activity.method = "UPDATE"
#             activity.application = "Account Permission"
#             activity.updatedDate = datetime.datetime.now()
#             activity.description = "Kullanıcı izni artık aktif değil. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#             activity.save()
#             instance.save()
#             messages.success(request, "Kullanıcı izni başarıyla etkisizleştirildi.")
#             return redirect("admin_account_permission")
#         else:
#             instance.isActive = False
#             messages.error(request, "Kullanıcı izni aktif.")
#             return redirect("admin_account_permission")
#     else:
#         messages.error(request, "Yetkiniz Yok!")
#
#

