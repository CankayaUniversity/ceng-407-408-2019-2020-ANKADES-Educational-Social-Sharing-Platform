from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
#Main View
from account.models import Account
from adminpanel.forms import AdminLoginForm


@login_required(login_url="login_admin")
def admin_index(request):
    if request.user.is_superuser:
        user = Account.objects.all()
        # article_count = Article.objects.all().count()
        # article_category_count = ArticleCategory.objects.all().count()
        # article_sub_category_count = ArticleSubCategory.objects.all().count()
        # article_comment_count = ArticleComment.objects.all().count()
        context = {
            "user": user,
            # "article_count": article_count,
            # "article_category_count": article_category_count,
            # "article_sub_category_count": article_sub_category_count,
            # "article_comment_count": article_comment_count,
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

