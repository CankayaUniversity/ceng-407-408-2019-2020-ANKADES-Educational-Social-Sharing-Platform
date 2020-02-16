from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Main View
from rest_framework import viewsets

from account.models import Account

# User View Set
from adminpanel.serializers import AccountSerializer

#Account View Set
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer

