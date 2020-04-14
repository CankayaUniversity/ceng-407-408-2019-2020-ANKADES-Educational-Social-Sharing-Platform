import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from online_users.models import OnlineUserActivity
from rest_framework.generics import get_object_or_404

from account.models import Account, Group, AccountGroup, Permission, AccountPermission
from account.views.views import current_user_group
from adminpanel.models import AdminLogs
from exam.models import School


@login_required(login_url="login_admin")
def admin_all_users(request):
    userGroup = current_user_group(request, request.user)
    accounts = Account.objects.all().order_by('-date_joined')
    context = {
        "userGroup": userGroup,
        "accounts": accounts,
    }
    return render(request, "adminpanel/account/all-users.html", context)


@login_required(login_url="login_admin")
def admin_active_users(request):
    userGroup = current_user_group(request, request.user)
    activeUsers = OnlineUserActivity.get_user_activities()
    context = {
        "userGroup": userGroup,
        "activeUsers": activeUsers,
    }
    return render(request, "adminpanel/account/online-users.html", context)


@login_required(login_url="login_admin")
def admin_all_user_groups(request):
    userGroup = current_user_group(request, request.user)
    admins = AccountGroup.objects.filter(Q(groupId__slug="admin"))
    moderators = AccountGroup.objects.filter(Q(groupId__slug="moderator"))
    teachers = AccountGroup.objects.filter(Q(groupId__slug="ogretmen"))
    students = AccountGroup.objects.filter(Q(groupId__slug="ogrenci"))
    members = AccountGroup.objects.filter(Q(groupId__slug="uye"))
    context = {
        "userGroup": userGroup,
        "admins": admins,
        "moderators": moderators,
        "teachers": teachers,
        "students": students,
        "members": members,
    }
    return render(request, "adminpanel/account/group/user-groups.html", context)


@login_required(login_url="login_admin")
def admin_my_account(request, username):
    userDetail = get_object_or_404(Account, username=username)
    userGroup = current_user_group(request, request.user)
    context = {
        "userDetail": userDetail,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/my-profile.html", context)


@login_required(login_url="login_admin")
def admin_students(request):
    userGroup = current_user_group(request, request.user)
    students = AccountGroup.objects.filter(Q(groupId__slug="ogrenci"))
    context = {
        "students": students,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/group/students.html", context)


@login_required(login_url="login_admin")
def admin_teachers(request):
    userGroup = current_user_group(request, request.user)
    teachers = AccountGroup.objects.filter(Q(groupId__slug="ogretmen"))
    context = {
        "teachers": teachers,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/group/teachers.html", context)


@login_required(login_url="login_admin")
def admin_moderators(request):
    userGroup = current_user_group(request, request.user)
    moderators = AccountGroup.objects.filter(Q(groupId__slug="moderator"))
    context = {
        "moderators": moderators,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/group/moderators.html", context)


@login_required(login_url="login_admin")
def admin_members(request):
    userGroup = current_user_group(request, request.user)
    members = AccountGroup.objects.filter(Q(groupId__slug="uye"))
    context = {
        "members": members,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/account/group/members.html", context)


@login_required(login_url="login_admin")
def admin_admins(request):
    admins = AccountGroup.objects.filter(groupId__slug="admin")
    moderators = AccountGroup.objects.filter(groupId__slug="moderator")
    teachers = AccountGroup.objects.filter(groupId__slug="ogretmen")
    students = AccountGroup.objects.filter(groupId__slug="ogrenci")
    userGroup = current_user_group(request, request.user)
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
    userGroup = current_user_group(request, request.user)
    instance = get_object_or_404(Account, username=request.user)
    schools = School.objects.filter(Q(isActive=False, isCategory=False))
    activity = AdminLogs()
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
        activity.creator = request.user.username
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı hesabını güncelledi."
        activity.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect(reverse("admin_edit_profile", kwargs={"username": username}))
    context = {
        "instance": instance,
        "userGroup": userGroup,
        "schools": schools,
    }
    return render(request, "adminpanel/account/edit-profile.html", context)


@login_required(login_url="login_admin")
def admin_edit_username(request, username):
    userGroup = current_user_group(request, request.user)
    instance = get_object_or_404(Account, username=username)
    activity = AdminLogs()
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
        activity.creator = request.user.username
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı kullanıcı adını güncelledi."
        activity.save()
        messages.success(request, "Kullanıcı adınız başarıyla güncellendi.")
        return redirect("admin_edit_username")
    return render(request, "adminpanel/account/edit-username.html", context)


@login_required(login_url="login_admin")
def admin_edit_email(request, username):
    userGroup = current_user_group(request, request.user)
    instance = get_object_or_404(Account, username=username)
    activity = AdminLogs()
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
            activity.title = "E-mail Güncelleme: " + str(request.user)
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = request.user.username
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı e-mail adresini güncelledi."
            activity.save()
            messages.success(request, "Email adresiniz başarıyla güncellendi.")
            return redirect("admin_edit_profile")
    return render(request, "adminpanel/account/edit-email.html", context)


@login_required(login_url="login_admin")
def admin_blocked_users(request):
    activity = AdminLogs()
    blockedUsers = Account.objects.filter(is_active=False)
    userGroup = current_user_group(request, request.user)
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
        activity.creator = request.user
        activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısının yetkisi yok."
        activity.save()
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")


@login_required(login_url="login_admin")
def admin_block_account(request, username):
    user = get_object_or_404(Account, username=username)
    userGroup = current_user_group(request, request.user)
    activity = AdminLogs()
    if userGroup == 'admin' or userGroup == 'moderator':
        if user.is_active is True:
            user.is_active = False
            user.save()
            activity.title = "Kullanıcı Engelleme"
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = request.user
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
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
            activity.creator = request.user
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı aktifleştirildi."
            activity.save()
            messages.success(request, "Kullanıcı başarıyla aktifleştirildi.")
            return redirect("admin_all_users")
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_all_users")


@login_required(login_url="login_admin")
def admin_delete_account(request, username):
    user = get_object_or_404(Account, username=username)
    userGroup = current_user_group(request, request.user)
    activity = AdminLogs()
    if userGroup == 'admin' or userGroup == 'moderator':
        if user.is_active is True:
            messages.error(request, "Kullanıcıyı silmek için engellemeniz gereklidir.")
            return redirect("admin_all_users")
        else:
            user.delete()
            activity.title = "Kullanıcı Silme"
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "DELETE"
            activity.creator = request.user
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcı sildi."
            activity.save()
            messages.success(request, "Kullanıcı başarıyla silindi.")
            return redirect("admin_all_users")
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_all_users")


@login_required(login_url="login_admin")
def admin_register_account(request):
    userGroup = current_user_group(request, request.user)
    accountGroup = AccountGroup()
    groups = Group.objects.all()
    activity = AdminLogs()
    context = {
        "userGroup": userGroup,
        "groups": groups,
    }
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        getGroup = request.POST['groupId']
        is_active = request.POST.get('is_active') == "on"
        if password and confirm_password and password != confirm_password:
            messages.error(request, "Girilen şifreler uyuşmuyor. Lütfen tekrar deneyin.")
            return render(request, "adminpanel/account/add-account.html", context)
        else:
            new_user = Account(first_name=first_name, last_name=last_name, username=username, email=email, is_active=is_active)
            new_user.save()
            new_user.set_password(password)
            new_user.save()
            accountGroup.userId_id = new_user.id
            accountGroup.groupId_id = getGroup
            accountGroup.save()
            if accountGroup.groupId.slug == 'admin':
                new_user.is_admin = True
                new_user.save()
            elif accountGroup.groupId.slug == 'moderator':
                new_user.is_staff = True
                new_user.save()
            activity.title = "Kullanıcı Ekleme"
            activity.application = "Account"
            activity.createdDate = datetime.datetime.now()
            activity.method = "UPDATE"
            activity.creator = request.user
            activity.description = "" + str(activity.createdDate) + " tarihinde, " + str(activity.creator) + " kullanıcısı eklendi."
            activity.save()
            messages.success(request, "Yeni kullanıcı başarıyla eklendi.")
            return redirect("admin_all_users")
    return render(request, "adminpanel/account/add-account.html", context)


@login_required(login_url="login_admin")
def admin_add_group_to_user(request):
    userGroup = current_user_group(request, request.user)
    groups = Group.objects.all()
    users = Account.objects.all()
    context = {
        "userGroup": userGroup,
        "groups": groups,
        "users": users,
    }
    activity = AdminLogs()
    if userGroup == 'admin':
        if request.method == "POST":
            userId = request.POST['userId']
            groupId = request.POST['groupId']
            try:
                getExistAccount = AccountGroup.objects.get(userId=userId)
                if getExistAccount:
                    getExistAccount.groupId_id = groupId
                    getExistAccount.save()
                    messages.success(request, "Kullanıcının grubu başarıyla değiştirildi.")
                    return redirect("admin_all_user_groups")
            except:
                instance = AccountGroup()
                instance.groupId_id = groupId
                instance.userId_id = userId
                instance.save()
                activity.creator = request.user
                activity.method = "POST"
                activity.createdDate = datetime.datetime.now()
                activity.application = "Account Group"
                activity.title = "Kullanıcıya Grup Ekleme"
                activity.description = str(instance.userId.get_full_name()) + " kullanıcısına " + str(
                    instance.groupId.title) + " grubu eklendi. İşlem tarihi: " + str(
                    activity.createdDate) + ". İşlemi gerçekleştiren kişi: " + str(activity.creator)
                activity.save()
                messages.success(request, "Kullanıcının grubu başarıyla değiştirildi.")
                return redirect("admin_dashboard")
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")
    return render(request, "adminpanel/account/group/add-group-to-user.html", context)


@login_required(login_url="login_admin")
def admin_add_permission_to_user(request):
    userGroup = current_user_group(request, request.user)
    permissions = Permission.objects.all()
    users = Account.objects.all()
    context = {
        "userGroup": userGroup,
        "permissions": permissions,
        "users": users,
    }
    activity = AdminLogs()
    if userGroup == 'admin':
        if request.method == "POST":
            userId = request.POST['userId']
            permissionId = request.POST['permissionId']
            try:
                getExistAccount = AccountPermission.objects.get(userId=userId, permissionId=permissionId)
                if getExistAccount:
                    messages.success(request, "Bu izin, kullanıcıya daha önce eklenmiş.")
                    return redirect("admin_all_user_permissions")
            except:
                instance = AccountPermission()
                instance.userId_id = userId
                instance.permissionId_id = permissionId
                instance.save()
                activity.creator = request.user
                activity.method = "POST"
                activity.createdDate = datetime.datetime.now()
                activity.application = "Account Permission"
                activity.title = "Kullanıcıya İzin Ekleme"
                activity.description = str(instance.userId.get_full_name()) + " kullanıcısına " + str(
                    instance.permissionId.title) + " izni eklendi. İşlem tarihi: " + str(
                    activity.createdDate) + ". İşlemi gerçekleştiren kişi: " + str(activity.creator)
                activity.save()
                messages.success(request, "Kullanıcının izni başarıyla eklendi.")
                return redirect("admin_dashboard")
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")
    return render(request, "adminpanel/account/permission/add-permission-to-user.html", context)
