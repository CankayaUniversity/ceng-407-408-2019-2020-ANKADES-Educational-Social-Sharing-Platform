from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404
from adminpanel.forms import AdminEditProfileForm, AccountPermissionForm

from account.models import Account, AccountGroup


#Kullanıcılar
@login_required(login_url="login_admin")
def admin_all_users(request):
    keyword = request.GET.get("keyword")
    if keyword:
        user_pagination = Account.objects.filter(
            Q(username__contains=keyword) |
            Q(first_name__contains=keyword) |
            Q(last_name__contains=keyword))
        context = {
            "user_pagination": user_pagination,
        }
        return render(request, "admin/account/all-users.html", context)

    user_groups = AccountGroup.objects.all()
    users_list = Account.objects.all()
    users_limit = Account.objects.all().order_by('-date_joined')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(users_limit, 5)
    try:
        user_pagination = paginator.page(page)
    except PageNotAnInteger:
        user_pagination = paginator.page(1)
    except EmptyPage:
        user_pagination = paginator.page(paginator.num_pages)

    context = {
        "users_list": users_list,
        "user_pagination": user_pagination,
        "users_limit": users_limit,
        "user_groups": user_groups,
    }
    return render(request, "admin/account/all-users.html", context)


@login_required(login_url="login_admin")
def admin_edit_profile(request, username):
    instance = get_object_or_404(Account, username=username)
    form = AdminEditProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.username = username
        instance.save()
        messages.success(request, "Profil başarıyla düzenlendi !")
        return redirect("admin_all_users")
    context = {
        "form": form,
    }
    return render(request, "admin/account/edit-profile.html", context)


@login_required(login_url="login_admin")
def admin_delete_profile(request, username):
    instance = get_object_or_404(Account, username=username)
    instance.delete()
    messages.success(request, "Profil başarıyla silindi !")
    return redirect("admin_all_users")


@login_required(login_url="login_admin")
def admin_blocked_users(request):
    blocked_user = Account.objects.all()
    context = {
        "blocked_user": blocked_user
    }
    return render(request, "admin/account/blocked-user.html", context)


#Kullanıcı izinleri
@login_required(login_url="login_admin")
def add_account_has_permission(request):
    form = AccountPermissionForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Kullanıcıya izin başarıyla eklendi !")
        return redirect("admin_index")
    context = {
        "form": form,
    }
    return render(request, "admin/permissions/add-account-has-per.html", context)