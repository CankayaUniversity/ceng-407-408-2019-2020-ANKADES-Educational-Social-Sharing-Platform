import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string

from ankadescankaya.views import current_user_group
from support.models import Report


@login_required(login_url="login_admin")
def add_report(request, getNumber):
    """
    :param getNumber:
    :param request:
    :return:
    """
    if request.method == "POST":
        description = request.POST.get("description")
        new_report = Report(description=description, isActive=True, isSolved=False, isRead=False, createdDate=datetime.datetime.now())
        new_report.supportNumber = get_random_string(length=32)
        new_report.title = "Kullanıcı Şikayeti"
        new_report.post = getNumber
        new_report.save()
        messages.success(request, "Şikayetiniz başarıyla gönderildi. En kısa sürede tarafınıza geri dönüş sağlanacaktır.")
        return redirect("index")
