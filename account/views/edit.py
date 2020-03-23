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
        username = request.POST.get("username")
        instance.first_name = first_name
        instance.last_name = last_name
        instance.username = username
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
def edit_username(request, username):
    """
    :param request:
    :param username:
    :return:
    """

    return None


@login_required(login_url="login_account")
def edit_password(request, username):
    if request.user.is_authenticated:
        user = get_object_or_404(Account, username=username)
        form = AccountUpdatePasswordForm(request.POST or None, request.user, instance=request.user)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = form.save(commit=False)
            update_session_auth_hash(request, username)
            user = request.user
            user.set_password(password)
            user.save()
            login_user = authenticate(username=username, password=password)
            login(request, login_user)
            messages.success(request, "Şifreniz başarıyla güncellendi.")
            return redirect("edit_profile")
        return render(request, "ankades/../../templates/test/account/edit-password.html", {"form": form})
    else:
        messages.error(request, "Bir sorun var, lütfen daha sonra tekrar deneyin")
        return redirect("login_account")