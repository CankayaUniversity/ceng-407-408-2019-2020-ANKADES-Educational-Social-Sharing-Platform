import datetime
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import RedirectView
from rest_framework.generics import get_object_or_404

from account.models import Account
from directmessage.forms import MessageForm
from directmessage.models import DirectMessage


def send_message(request, username):
    return None