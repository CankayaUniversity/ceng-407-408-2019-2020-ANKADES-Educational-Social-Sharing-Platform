from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from rest_framework import viewsets
from account.models import Account, AccountGroup
from adminpanel.forms import AdminLoginForm, AddAccountHasPermission
from adminpanel.models import AdminActivity
from adminpanel.serializers import AccountPermissionsSerializer, AccountGroupsSerializer, AdminActivitySerializer
from course.models import CourseCategory, CourseSubCategory, Course, CourseSubToSubCategory


# UserViewSet
class AccountGroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = AccountGroupsSerializer


class AccountPermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = AccountPermissionsSerializer


class AdminActivityViewSet(viewsets.ModelViewSet):
    queryset = AdminActivity.objects.all()
    serializer_class = AdminActivitySerializer


# Dashboard View
@login_required(login_url="login_admin")
def admin_index(request):
    if request.user.is_superuser:
        user = Account.objects.all()
        admin = AccountGroup.objects.filter(group_id__name__contains="Admin")
        moderator = AccountGroup.objects.filter(group_id__name__contains="Moderatör")
        ogretmen = AccountGroup.objects.filter(group_id__name__contains="Öğretmen")
        ogrenci = AccountGroup.objects.filter(group_id__name__contains="Öğrenci")
        user_count = Account.objects.all().count()
        course_count = Course.objects.all().count()
        course_category_count = CourseCategory.objects.all().count()
        course_sub_category_count = CourseSubCategory.objects.all().count()
        course_sub_to_sub_category_count = CourseSubToSubCategory.objects.all().count()
        activity = AdminActivity.objects.all()
        activity_limit = AdminActivity.objects.all().order_by("-act_created_date")[:4]
        context = {
            "user": user,
            "ogrenci": ogrenci,
            "moderator": moderator,
            "ogretmen": ogretmen,
            "admin": admin,
            "user_count": user_count,
            "course_count": course_count,
            "course_category_count": course_category_count,
            "course_sub_category_count": course_sub_category_count,
            "course_sub_to_sub_category_count": course_sub_to_sub_category_count,
            "activity": activity,
            "activity_limit": activity_limit,
        }
        return render(request, "admin/index.html", context)
    else:
        return redirect("admin_index")


# User View
def login_admin(request):
    if not request.user.is_authenticated:
        form = AdminLoginForm(request.POST or None)
        context = {
            "form": form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is None:
                return render(request, "admin/login.html", context)
            else:
                if user.is_active and user.is_superuser:
                    login(request, user)
                    return redirect("admin_index")
                else:
                    return render(request, "admin/login.html", context)
        else:
            return render(request, "admin/login.html", context)
    else:
        return redirect("admin_index")


@login_required(login_url="login_admin")
def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login_admin")
    else:
        return redirect("login_admin")








