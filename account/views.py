from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets

from account.forms import AccountLoginForm, AccountRegisterForm
from account.models import Account, Group, AccountGroup, Permission, AccountPermission, GroupPermission, AccountActivity
from adminpanel.models import AdminActivity

from adminpanel.serializers import AccountSerializer, GroupSerializer, AccountGroupSerializer, PermissionSerializer, \
    AccountPermissionSerializer, GroupPermissionSerializer, AccountActivitySerializer, AdminActivitySerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('-date_joined')
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-createdDate')
    serializer_class = GroupSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer


class AccountPermissionViewSet(viewsets.ModelViewSet):
    queryset = AccountPermission.objects.all().order_by('-createdDate')
    serializer_class = AccountPermissionSerializer


class GroupPermissionViewSet(viewsets.ModelViewSet):
    queryset = GroupPermission.objects.all().order_by('-createdDate')
    serializer_class = GroupPermissionSerializer


class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all().order_by('-createdDate')
    serializer_class = AccountGroupSerializer


class AccountActivityViewSet(viewsets.ModelViewSet):
    queryset = AccountActivity.objects.all().order_by('-activityCreatedDate')
    serializer_class = AccountActivitySerializer


class AdminActivityViewSet(viewsets.ModelViewSet):
    queryset = AdminActivity.objects.all().order_by('-activityCreatedDate')
    serializer_class = AdminActivitySerializer


def index(request):
    return render(request, "ankades/index.html")


def login_account(request):
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
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Başarıyla çıkış yapıldı")
        return redirect("login_account")
    else:
        return redirect("index")


def register_account(request):
    if not request.user.is_authenticated:
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
            messages.success(request, "Kayıt işlemi başarıyla gerçekleştirildi.")
            login(request, new_user)
            if login:
                messages.success(request, "Başarıyla giriş yapıldı.")
            else:
                messages.error(request, "Giriş yapılırken bir sorun oluştu.")
            return redirect("login_account")
        context = {
            "form": form
        }
        return render(request, "ankades/account/register.html", context)
    else:
        messages.error(request, "Zaten giriş yapılmış.")
        return redirect("index")
