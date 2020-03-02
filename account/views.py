import datetime
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from account.forms import AccountRegisterForm, EditProfileForm, AccountLoginForm
from account.models import Account, AccountGroup, Group


def login_account(request):
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        form = AccountLoginForm(request.POST or None)
        context = {
            "form": form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, "ankades/account/login.html", context)
            else:
                login(request, user)
                messages.success(request, "Başarıyla giriş yapıldı.")
                return redirect("index")
        else:
            return render(request, "ankades/account/login.html", context)
    else:
        return redirect("index")


@login_required(login_url="login_account")
def logout_account(request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yapıldı")
        return redirect("index")
    else:
        return redirect("index")


def register_account(request):
    """
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        getGroup = Group.objects.get(slug="ogrenci")
        accountGroup = AccountGroup()
        form = AccountRegisterForm(request.POST or None)
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
            return redirect("login_account")
        context = {
            "form": form
        }
        return render(request, "ankades/account/register.html", context)
    else:
        messages.error(request, "Zaten giriş yapılmış.")
        return redirect("index")

def account_detail(request, username):
    userDetail = get_object_or_404(Account, username=username)
    userOccupation = AccountGroup.objects.get(userId__username=username)
    context = {
        "userDetail": userDetail,
        "userOccupation": userOccupation,
    }
    return render(request, "ankades/account/account-detail.html", context)


@login_required(login_url="login_account")
def edit_profile(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    instance = get_object_or_404(Account, username=username)
    form = EditProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.username = username
        instance.save()
        messages.success(request, "Profil başarıyla düzenlendi !")
        return redirect("edit_profile")
    context = {
        "form": form,
    }
    return render(request, "ankades/account/edit-profile.html", context)


def index(request):
    """
    :param request:
    :return:
    """
    return render(request, "ankades/index.html")