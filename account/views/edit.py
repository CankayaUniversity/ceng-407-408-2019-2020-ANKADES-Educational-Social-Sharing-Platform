import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from account.forms import AccountUpdatePasswordForm, EditProfileForm
from account.models import Account, AccountActivity
from account.views.views import current_user_group


@login_required(login_url="login_account")
def edit_profile(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        instance.first_name = first_name
        instance.last_name = last_name
        if request.FILES:
            media = request.FILES.get('media')
            fs = FileSystemStorage()
            fs.save(media.name, media)
            instance.image = media
        instance.save()
        activity.title = "Profil Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(activity.creator) + " kullanıcısı hesabını güncelledi."
        activity.save()
        messages.success(request, "Profil başarıyla güncellendi.")
        return redirect(reverse("account_detail", kwargs={"username": currentUser}))
    context = {
        "instance": instance,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "ankades/account/edit-profile.html", context)


@login_required(login_url="login_account")
def edit_username(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    if request.method == "POST":
        username = request.POST.get("username")
        instance.username = username
        instance.save()
        activity.title = "KUllanıcı Adı Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı kullanıcı adını güncelledi."
        activity.save()
        messages.success(request, "Kullanıcı adı başarıyla güncellendi.")
        return redirect("index")
    context = {
        "instance": instance,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "ankades/account/edit-profile.html", context)


# @login_required(login_url="login_account")
# def edit_password(request):
#     currentUser = request.user
#     if request.user.is_authenticated:
#         user = get_object_or_404(Account, username=currentUser)
#         form = AccountUpdatePasswordForm(request.POST or None, request.user, instance=request.user)
#         currentUser = request.user
#         instance = get_object_or_404(Account, username=currentUser)
#         activity = AccountActivity()
#         if form.is_valid():
#             password = form.cleaned_data.get("password")
#             user = form.save(commit=False)
#             update_session_auth_hash(request, username)
#             user = request.user
#             user.set_password(password)
#             user.save()
#             login_user = authenticate(username=username, password=password)
#             login(request, login_user)
#             activity.title = "Parola Güncelleme."
#             activity.application = "Account"
#             activity.method = "UPDATE"
#             activity.creator = currentUser
#             activity.description = str(activity.createdDate) + " tarihinde, " + str(
#                 activity.creator) + " kullanıcısı parolasını güncelledi."
#             activity.save()
#             messages.success(request, "Parolanız başarıyla güncellendi.")
#             return redirect("edit_profile")
#         return render(request, "ankades/../../templates/test/account/edit-password.html", {"form": form})
#     else:
#         messages.error(request, "Bir sorun var, lütfen daha sonra tekrar deneyin")
#         return redirect("login_account")


@login_required(login_url="login_account")
def edit_email(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    instance = get_object_or_404(Account, username=currentUser)
    activity = AccountActivity()
    if request.method == "POST":
        email = request.POST.get("email")
        instance.email = email
        instance.save()
        activity.title = "Email Güncelleme."
        activity.application = "Account"
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(activity.creator) + " kullanıcısı email adresini güncelledi."
        activity.save()
        messages.success(request, "Email başarıyla güncellendi.")
        return redirect(reverse("account_detail", kwargs={"username": currentUser}))
    context = {
        "instance": instance,
        "currentUser": currentUser.username,
        "userGroup": userGroup,
    }
    return render(request, "ankades/account/edit-profile.html", context)