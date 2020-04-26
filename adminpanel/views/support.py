import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ankadescankaya.views import current_user_group
from support.models import Support


@login_required(login_url="login_account")
def admin_add_support_subject(request):
    userGroup = current_user_group(request, request.user)
    if userGroup == "admin":
        if request.method == "POST":
            title = request.POST.get("title")
            description = request.POST.get("description")
            isActive = request.POST.get("isActive") == "on"
            isRoot = request.POST.get("isRoot") == "on"
            isCategory = request.POST.get("isCategory") == "on"
            new_support_subject = Support(title=title, description=description, isActive=isActive, isRoot=isRoot, isCategory=isCategory)
            new_support_subject.createdDate = datetime.datetime.now()
            new_support_subject.creator = request.user
            new_support_subject.save()
            new_support_subject.parentId = new_support_subject
            new_support_subject.save()
            messages.success(request, "Destek Başlığı başarıyla oluşturuldu.")
        return render(request, "adminpanel/article/add-support-subject.html", {"userGroup": userGroup})
    else:
        messages.error(request, "Yetkiniz yok.")
        return redirect("admin_dashboard")
