import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from ankadescankaya.views.views import current_user_group
from article.forms import ArticleForm
from article.models import Article, ArticleCategory


@login_required(login_url="login_admin")
def admin_all_articles(request):
    """
    :param request:
    :return:
    """
    articles = Article.objects.all()
    userGroup = current_user_group(request, request.user)
    context = {
        "articles": articles,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/article/all-articles.html", context)


@login_required(login_url="login_admin")
def admin_isactive_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    if instance.isActive is True:
        instance.isActive = False
        instance.save()
        messages.success(request, "Makale artık aktif değil.")
        return redirect("admin_all_articles")
    else:
        instance.isActive = True
        instance.save()
        messages.success(request, "Makale başarıyla aktifleştirildi.")
        return redirect("admin_all_articles")


@login_required(login_url="login_admin")
def admin_delete_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    userGroup = current_user_group(request, request.user)
    if userGroup == 'admin':
        if instance.isActive is True:
            messages.error(request, "Makale aktif olduğu için silme işlemi gerçekleştirilemedi.")
            return redirect("admin_all_articles")
        else:
            instance.delete()
            messages.success(request, "Makale başarıyla silindi.")
            return redirect("admin_all_articles")
    else:
        messages.error(request, "Yetkiniz Yok.")
        return redirect("all_articles")


@login_required(login_url="login_admin")
def admin_add_article_category(request):
    """
    :param request:
    :return:
    """
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=True)).order_by('title')
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
        "articleCategory": articleCategory
    }
    if userGroup == 'admin':
        if request.method == "POST":
            value = request.POST['categoryId']
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == "on"
            isCategory = request.POST.get("isCategory") == "on"
            try:
                getTitle = ArticleCategory.objects.get(title=title)
                if title:
                    messages.error(request, "Eklemek istediğiniz kategori zaten mevcut.")
                    return redirect("admin_add_article_category")
                return render(request, "adminpanel/article/add-category.html", context)
            except:
                instance = ArticleCategory(title=title, isActive=isActive, isCategory=isCategory)
                instance.creator = request.user
                # jsonField = {"childId": instance.id}
                # instance.parentId.tree = json.dumps(jsonField)ç
                instance.parentId_id = value
                instance.save()
                messages.success(request, "Makale kategorisi başarıyla eklendi !")
                return redirect("admin_add_article_category")
        return render(request, "adminpanel/article/add-category.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_article_categories")


@login_required(login_url="login_admin")
def admin_edit_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    instance = Article.objects.get(slug=slug)
    form = ArticleForm(request.POST or None)
    context = {
        "articleCategory": articleCategory,
        "userGroup": userGroup,
        "form": form,
    }
    if request.method == "POST":
        value = request.POST['categoryId']
        title = request.POST.get("title")
        isPrivate = request.POST.get("isPrivate") == "on"
        isActive = request.POST.get("isActive") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
        instance.isActive = isActive
        instance.title = title
        instance.categoryId_id = value
        instance.updatedDate = datetime.datetime.now()
        if request.FILES:
            media = request.FILES.get('media')
            fs = FileSystemStorage()
            fs.save(media.name, media)
            instance.media = media
        else:
            instance.media = instance.media
        instance.save()
        messages.success(request, "Makale başarıyla düzenlendi !")
        return render(request, "adminpanel/article/edit-article.html", context)
    return render(request, "adminpanel/article/edit-article.html", context)


@login_required(login_url="login_admin")
def admin_article_categories(request):
    """
    :param request:
    :return:
    """
    request.user = request.user
    userGroup = current_user_group(request, request.user)
    categories = ArticleCategory.objects.all()
    context = {
        "categories": categories,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/article/categories.html", context)


@login_required(login_url="login_admin")
def admin_isactive_article_category(request, slug):
    request.user = request.user
    userGroup = current_user_group(request, request.user)
    try:
        instance = ArticleCategory.objects.get(slug=slug)
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.save()
                messages.success(request, "Makale kategorisi artık aktif değil.")
                return redirect("admin_article_categories")
            else:
                instance.isActive = True
                instance.save()
                messages.success(request, "Makale kategorisi başarıyla aktifleştirildi.")
                return redirect("admin_article_categories")
        else:
            messages.error(request, "Yetkiniz yok.")
            return redirect("admin_article_categories")
    except:
        return render(request, "404.html")


@login_required(login_url="login_admin")
def admin_delete_article_category(request, slug):
    instance = get_object_or_404(ArticleCategory, slug=slug)
    if instance.isActive is True:
        messages.error(request, "Makale kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
        return redirect("admin_article_categories")
    else:
        instance.delete()
        messages.success(request, "Makale kategorisi başarıyla silindi.")
        return redirect("admin_article_categories")
