import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import AccountGroup, Account
from account.views.views import current_user_group
from adminpanel.forms import AdminArticleForm, AdminArticleCategoryForm, AdminEditArticleCategoryForm, \
    AdminEditArticleForm, AddArticleForm
from adminpanel.models import AdminActivity
from article.models import Article, ArticleCategory


@login_required(login_url="login_admin")
def admin_all_articles(request):
    """
    :param request:
    :return:
    """
    articles = Article.objects.all()
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "articles": articles,
        "adminGroup": adminGroup,
        "currentUser": currentUser,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/article/all-articles.html", context)


@login_required(login_url="login_admin")
def admin_add_article(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    form = AddArticleForm(request.POST or None)
    activity = AdminActivity()
    context = {
        "articleCategory": articleCategory,
        "userGroup": userGroup,
        "currentUser": currentUser,
        "form": form,
    }
    if request.method == "POST":
        value = request.POST['id']
        title = request.POST.get("title")
        if form.is_valid():
            description = form.cleaned_data.get("description")
        isPrivate = request.POST.get("isPrivate") == "on"
        isActive = request.POST.get("isActive") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
        if not title and description:
            messages.error(request, "Kategori, Başlık ve Açıklama kısımları boş geçilemez")
            return render(request, "adminpanel/article/add-article.html", context)
        instance = Article(title=title, description=description,
                           isPrivate=isPrivate, isActive=isActive)
        if request.FILES:
            media = request.FILES.get('media')
            fs = FileSystemStorage()
            fs.save(media.name, media)
            instance.media = media
        instance.creator = request.user
        instance.categoryId_id = value
        instance.isActive = True
        instance.save()
        activity.title = "Makale Ekleme: " + str(currentUser)
        activity.application = "Article"
        activity.createdDate = datetime.datetime.now()
        activity.method = "INSERT"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı makale ekledi."
        activity.save()
        messages.success(request, "Makale başarıyla eklendi !")
        return redirect("admin_dashboard")
    return render(request, "adminpanel/article/add-article.html", context)


@login_required(login_url="login_admin")
def admin_isactive_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    if instance.isActive is True:
        instance.isActive = False
        instance.save()
        activity.title = "Makale aktifleştirme: " + str(currentUser)
        activity.application = "Article"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı makale aktifliği kaldırıldı."
        activity.save()
        messages.success(request, "Makale artık aktif değil.")
        return redirect("admin_all_articles")
    else:
        instance.isActive = True
        instance.save()
        activity.title = "Makale Aktifleştirme: " + str(currentUser)
        activity.application = "Article"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı makaleyi aktifleştirdi."
        activity.save()
        messages.success(request, "Makale başarıyla aktifleştirildi.")
        return redirect("admin_all_articles")


@login_required(login_url="login_admin")
def admin_delete_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    if instance.isActive is True:
        messages.error(request, "Makale aktif olduğu için silme işlemi gerçekleştirilemedi.")
        return redirect("admin_all_articles")
    else:
        instance.delete()
        messages.success(request, "Makale başarıyla silindi.")
        return redirect("admin_all_articles")


@login_required(login_url="login_admin")
def admin_add_article_category(request):
    """
    :param request:
    :return:
    """
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=True))
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    context = {
        "userGroup": userGroup,
        "currentUser": currentUser,
        "articleCategory": articleCategory
    }
    if userGroup == 'admin':
        if request.method == "POST":
            value = request.POST.get("value")
            title = request.POST.get("title")
            isActive = request.POST.get("isActive") == "on"
            isCategory = request.POST.get("isCategory") == "on"
            instance = ArticleCategory(parentId=value, title=title, isActive=isActive, isCategory=isCategory)
            instance.creator = request.user
            instance.save()
            activity.title = "Makale Kategorisi Ekleme: " + str(currentUser)
            activity.application = "Article"
            activity.createdDate = datetime.datetime.now()
            activity.method = "INSERT"
            activity.creator = currentUser
            activity.description = str(activity.createdDate) + " tarihinde, " + str(
                activity.creator) + " kullanıcısı makale için kategori ekledi."
            activity.save()
            messages.success(request, "Makale kategorisi başarıyla eklendi !")
            return redirect("admin_add_article_category")
        return render(request, "adminpanel/article/add-category.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("admin_dashboard")
#
#
# @login_required(login_url="login_admin")
# def admin_edit_article(request, slug):
#     """
#     :param request:
#     :param slug:
#     :return:
#     """
#     instance = get_object_or_404(Article, slug=slug)
#     activity = AdminActivity()
#     form = AdminEditArticleForm(request.POST or None, request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.creator = request.user
#         instance.updatedDate = datetime.datetime.now()
#         activity.title = "Makale düzenlendi"
#         activity.creator = request.user.username
#         activity.method = "PUT"
#         activity.application = "Article"
#         activity.updatedDate = datetime.datetime.now()
#         activity.description = "Makale düzenlendi. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#         activity.save()
#         instance.save()
#         messages.success(request, "Makale başarıyla düzenlendi !")
#         context = {
#             "form": form,
#         }
#         return render(request, "admin/article/edit-article.html", context)
#     return render(request, "admin/article/edit-article.html", {"form": form})
#
#
# @login_required(login_url="login_admin")
# def admin_delete_article(request, slug):
#     """
#     :param request:
#     :param slug:
#     :return:
#     """
#     instance = get_object_or_404(Article, slug=slug)
#     activity = AdminActivity()
#     if instance.isActive is True:
#         instance.isActive = False
#         activity.title = "Makale etkisizleştirildi"
#         activity.creator = request.user.username
#         activity.method = "PUT"
#         activity.application = "Article"
#         activity.updatedDate = datetime.datetime.now()
#         activity.description = "Makale etkisizleştirildi. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#         activity.save()
#         instance.save()
#         messages.success(request, "Makale başarıyla silindi !")
#         return redirect("admin_articles")
#     else:
#         messages.error(request, "Makale aktif değil")
#         activity.title = "Makale etkisizleştirilmedi"
#         activity.creator = request.user.username
#         activity.method = "PUT"
#         activity.application = "Article"
#         activity.updatedDate = datetime.datetime.now()
#         activity.description = "Makale etkisizleştirilmedi(zaten aktif değil). İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#         activity.save()
#         return redirect("admin_articles")


@login_required(login_url="login_admin")
def admin_article_categories(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    categories = ArticleCategory.objects.all()
    article_categories_limit = ArticleCategory.objects.all().order_by('-createdDate')[:5]
    adminGroup = AccountGroup.objects.filter(userId__username=request.user.username, groupId__slug="admin")
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "article_categories_limit": article_categories_limit,
        "adminGroup": adminGroup,
        "currentUser": currentUser,
    }
    return render(request, "adminpanel/article/categories.html", context)


@login_required(login_url="login_admin")
def admin_isactive_article_category(request, slug):
    instance = get_object_or_404(ArticleCategory, slug=slug)
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    activity = AdminActivity()
    if instance.isActive is True:
        instance.isActive = False
        instance.save()
        activity.title = "Makale Kategorisini Aktifleştirme: " + str(currentUser)
        activity.application = "Article"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı makale kategorisinin aktifliğini kaldırdı."
        activity.save()
        messages.success(request, "Makale kategorisi artık aktif değil.")
        return redirect("admin_article_categories")
    else:
        instance.isActive = True
        instance.save()
        activity.title = "Makale Kategorisini Aktifleştirme: " + str(currentUser)
        activity.application = "Article"
        activity.createdDate = datetime.datetime.now()
        activity.method = "UPDATE"
        activity.creator = currentUser
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı makale kategorisini aktifleştirdi."
        activity.save()
        messages.success(request, "Makale kategorisi başarıyla aktifleştirildi.")
        return redirect("admin_article_categories")


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
#
# @login_required(login_url="login_admin")
# def admin_edit_article_category(request, slug):
#     """
#     :param request:
#     :param slug:
#     :return:
#     """
#     instance = get_object_or_404(ArticleCategory, slug=slug)
#     activity = AdminActivity()
#     form = AdminEditArticleCategoryForm(request.POST or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.updatedDate = datetime.datetime.now()
#         activity.title = "Makale kategori güncelleme"
#         activity.creator = request.user.username
#         activity.method = "PUT"
#         activity.application = "Article Category"
#         activity.updatedDate = datetime.datetime.now()
#         activity.description = "Makale kategori düzenlendi. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#         activity.save()
#         instance.save()
#         messages.success(request, "Makale kategorisi başarıyla düzenlendi !")
#         return redirect("admin_edit_article_category", slug)
#     return render(request, "admin/article/edit-category.html", {"form": form})
#
#
# @login_required(login_url="login_admin")
# def admin_delete_article_category(request, slug):
#     """
#     :param request:
#     :param slug:
#     :return:
#     """
#     instance = get_object_or_404(ArticleCategory, slug=slug)
#     activity = AdminActivity()
#     if instance.isActive is True:
#         instance.isActive = False
#         activity.title = "Makale etkisizleştirildi"
#         activity.creator = request.user.username
#         activity.method = "PUT"
#         activity.application = "Article Category"
#         activity.updatedDate = datetime.datetime.now()
#         activity.description = "Makale kategori etkisizleştirildi. İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#         activity.save()
#         instance.save()
#         messages.success(request, "Makale kategorisi başarıyla etkisizleştirildi !")
#         return redirect("admin_article_category")
#     else:
#         messages.error(request, "Makale kategorisi zaten aktif değil!")
#         activity.title = "Makale kategori etkisizleştirilmedi"
#         activity.creator = request.user.username
#         activity.method = "PUT"
#         activity.application = "Article"
#         activity.updatedDate = datetime.datetime.now()
#         activity.description = "Makale kategori etkisizleştirilmedi(zaten aktif değil). İşlemi yapan kişi: " + activity.creator + " Uygulama adı: " + activity.application
#         activity.save()
#         return redirect("admin_article_category")
#
#
# def admin_edit_tag(request, slug):
#     return None
#
#
# def admin_delete_tag(request):
#     return None