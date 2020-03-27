from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.views.views import current_user_group


@login_required(login_url="login_account")
def account_detail(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    userDetail = get_object_or_404(Account, username=username)
    if request.user.is_authenticated:
        currentUser = request.user
        userGroup = current_user_group(request, username)
        context = {
            "userDetail": userDetail,
            "userGroup": userGroup,
            "currentUser": currentUser,
        }
    else:
        context = {
            "userDetail": userDetail,
        }
    return render(request, "ankades/account/account-detail.html", context)