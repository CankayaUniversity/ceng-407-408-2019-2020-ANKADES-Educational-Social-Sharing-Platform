from django.shortcuts import render

from account.views.views import current_user_group


def index(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    if userGroup is None:
        userGroup = 'Kullanıcı'
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup
    }
    return render(request, "ankades/dashboard.html", context)
