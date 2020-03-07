import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import AccountGroup
from adminpanel.forms import AdminArticleForm, AdminArticleCategoryForm, AdminTagForm, AdminEditArticleCategoryForm
from adminpanel.models import Tag
from article.models import Article, ArticleCategory, ArticleTag


@login_required(login_url="login_admin")
def admin_articles(request):
    """
    :param request:
    :return:
    """
    articles = Article.objects.all()
    context = {
        "articles": articles,
    }
    return render(request, "admin/article/all-articles.html", context)


@login_required(login_url="login_admin")
def admin_tags(request):
    """
    :param request:
    :return:
    """
    tags = Tag.objects.all()
    context = {
        "tags": tags,
    }
    return render(request, "admin/tags/all-tags.html", context)


@login_required(login_url="login_admin")
def admin_add_article(request):
    """
    :param request:
    :return:
    """
    form = AdminArticleForm(request.POST or None)
    context = {
        "form": form
    }
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
            form_username = form.cleaned_data.get("userId")
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.save()
            messages.success(request, "Makale başarıyla eklendi !")
            return redirect("admin_articles")
        return render(request, "admin/article/add-article.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_add_article_category(request):
    """
    :param request:
    :return:
    """
    form = AdminArticleCategoryForm(request.POST or None)

    context = {
        "form": form,
    }
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    if adminGroup:
        if form.is_valid():
            parentId = form.cleaned_data.get("parentId")
            isCategory = form.cleaned_data.get("isCategory")
            title = form.cleaned_data.get("title")
            slug = form.cleaned_data.get("slug")
            isActive = form.cleaned_data.get("isActive")
            instance = ArticleCategory(parentId=parentId, isCategory=isCategory, isActive=isActive, title=title, slug=slug)
            instance.creator = request.user
            instance.save()
            messages.success(request, "Makale kategorisi başarıyla eklendi !")
            return redirect("admin_add_article_category")
        return render(request, "admin/article/add-category.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_index")


@login_required(login_url="login_admin")
def admin_add_tag(request):
    """
    :param request:
    :return:
    """
    form = AdminTagForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Etiket başarıyla eklendi !")
        return redirect("admin_articles")
    return render(request, "admin/article/add-tag.html", context)


@login_required(login_url="login_admin")
def admin_edit_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    if request.user.is_authenticated:
        instance = get_object_or_404(Article, slug=slug)
        form = AdminArticleForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updatedDate = datetime.datetime.now()
            instance.save()
            messages.success(request, "Makale başarıyla düzenlendi !")
            context = {
                "form": form,
            }
            return render(request, "admin/article/edit-article.html", context)
        return render(request, "admin/article/edit-article.html", {"form": form})
    else:
        return redirect("login_admin")


@login_required(login_url="login_admin")
def admin_delete_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Article, slug=slug)
    instance.delete()
    messages.success(request, "Makale başarıyla silindi !")
    return redirect("admin_courses")


@login_required(login_url="login_admin")
def admin_article_category(request):
    """
    :param request:
    :return:
    """
    article_categories_list = ArticleCategory.objects.all()
    article_categories_limit = ArticleCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "article_categories_list": article_categories_list,
        "article_categories_limit": article_categories_limit,
    }
    return render(request, "admin/article/all-categories.html", context)


@login_required(login_url="login_admin")
def admin_edit_article_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(ArticleCategory, slug=slug)
    form = AdminEditArticleCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Kurs kategorisi başarıyla düzenlendi !")
        return redirect("admin_edit_article_category", slug)
    return render(request, "admin/article/edit-category.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_article_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(ArticleCategory, slug=slug)
    if instance.isActive is True:
        instance.isActive = False
        messages.success(request, "Kurs kategorisi başarıyla etkisizleştirildi !")
        return redirect("admin_article_category")
    else:
        messages.error(request, "Kurs kategorisi zaten aktif değil!")
        return redirect("admin_article_category")
