from django.shortcuts import render

from account.views.views import current_user_group


def index(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = 'Kullanıcı'
    if request.user.is_authenticated:
        userGroup = current_user_group(request, currentUser)
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup
    }
    return render(request, "ankades/dashboard.html", context)