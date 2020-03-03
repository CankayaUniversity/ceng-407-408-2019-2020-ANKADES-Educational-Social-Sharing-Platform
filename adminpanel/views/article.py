import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from adminpanel.forms import AdminArticleForm, AdminArticleCategoryForm
from article.models import Article, ArticleCategory


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
def admin_add_article(request):
    """
    :param request:
    :return:
    """
    form = AdminArticleForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Makale başarıyla eklendi !")
        return redirect("admin_articles")
    return render(request, "admin/article/add-article.html", context)


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
            instance.view += 5
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
def admin_add_article_category(request):
    """
    :param request:
    :return:
    """
    form = AdminArticleCategoryForm(request.POST or None)

    context = {
        "form": form,
    }
    if form.is_valid():
        categoryId = forms.cleaned_data.get("categoryId")
        isCategory = form.cleaned_data.get("isCategory")
        title = form.cleaned_data.get("title")
        slug = form.cleaned_data.get("slug")
        isActive = form.cleaned_data.get("isActive")
        instance = AdminArticleCategoryForm(categoryId=categoryId, isCategory=isCategory, isActive=isActive,
                                            title=title, slug=slug)
        instance.creator = request.user
        instance.save()
        messages.success(request, "Makale kategorisi başarıyla eklendi !")
        return redirect("admin_add_article_category")
    return render(request, "admin/article/add-category.html", context)


@login_required(login_url="login_admin")
def admin_edit_article_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(ArticleCategory, slug=slug)
    form = AdminArticleCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Kurs kategorisi başarıyla düzenlendi !")
        return redirect("admin_edit_article_category")
    return render(request, "admin/article/edit-category.html", {"form": form})


@login_required(login_url="login_admin")
def admin_delete_article_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(ArticleCategory, slug=slug)
    instance.delete()
    messages.success(request, "Makale kategorisi başarıyla silindi !")
    return redirect("admin_articles")
