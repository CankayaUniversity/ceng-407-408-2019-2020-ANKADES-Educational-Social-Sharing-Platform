from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Main View
from rest_framework import viewsets

from account.forms import AccountLoginForm
from account.models import Account, AccountActivity

# User View Set
from account.serializers import AccountActivitySerializer
from adminpanel.serializers import AccountSerializer

#Account View Set
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer


class AccountActivityViewSet(viewsets.ModelViewSet):
    queryset = AccountActivity.objects.all()
    serializer_class = AccountActivitySerializer


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
                return redirect("index")
        else:
            return render(request, "ankades/account/login.html", context)
    else:
        return redirect("index")


@login_required(login_url="login_account")
def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login_account")
    else:
        return redirect("login_account")