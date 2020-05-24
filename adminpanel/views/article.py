import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.db.models.signals import pre_save
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.generic import DetailView
from rest_framework.generics import get_object_or_404

from ankadescankaya.slug import slug_save
from ankadescankaya.views.views import current_user_group
from article.forms import EditArticleForm
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
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(Article, slug=slug)
    if instance.isActive is True:
        instance.isActive = False
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Makale artık aktif değil.")
        return redirect("admin_all_articles")
    else:
        instance.isActive = True
        instance.updatedDate = datetime.datetime.now()
        instance.save()
        messages.success(request, "Makale başarıyla aktifleştirildi.")
        return redirect("admin_all_articles")


@login_required(login_url="login_admin")
def admin_delete_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
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
        return redirect("admin_all_articles")


@login_required(login_url="login_admin")
def admin_add_article_category(request):
    """
    :param request:
    :return:
    """
    topCategory = ArticleCategoryView.getTopCategory(request)
    userGroup = current_user_group(request, request.user)
    context = {
        "userGroup": userGroup,
        "topCategory": topCategory
    }
    if userGroup == 'admin' or userGroup == 'moderator':
        getTop = request.GET.get('getTop')
        postTop = request.POST.get('postTop')
        home = request.POST.get('home')
        if getTop or home or postTop:
            if home:  # If request category slug is equal to home
                parent = ArticleCategory.objects.get(catNumber=home)
                if request.method == 'POST':
                    title = request.POST.get('title')
                    isActive = request.POST.get("isActive") == 'on'
                    new_cat = ArticleCategory(creator=request.user, isCategory=True, isActive=isActive, isRoot=False, parentId=parent, title=title)
                    new_cat.catNumber = "c-" + get_random_string(length=7)
                    new_cat.createdDate = datetime.datetime.now()
                    new_cat.creator = request.user
                    new_cat.save()
                    messages.success(request, "Makale için üst kategori başarıyla eklendi.")
                    return redirect("admin_add_article_category")
            if getTop == 'c-IGfbPX':
                home = ArticleCategory.objects.get(catNumber=getTop)
                context = {
                    "getTop": getTop,
                    "userGroup": userGroup,
                    "home": home
                }
                return render(request, "adminpanel/article/add-category.html", context)
            if postTop:
                inputTop = ArticleCategory.objects.get(catNumber=postTop)
                selectSub = ArticleCategory.objects.filter(parentId=inputTop)
                context = {
                    "getTop": getTop,
                    "inputTop": inputTop,
                    "selectSub": selectSub,
                    "userGroup": userGroup,
                }
                if request.method == 'POST':
                    selection = request.POST.get('selection')
                    if selection == 'none':
                        title = request.POST.get('title')
                        isActive = request.POST.get("isActive") == 'on'
                        new_top = ArticleCategory(title=title, isCategory=True, isActive=isActive, isRoot=False, parentId=inputTop)
                        new_top.catNumber = "c-" + get_random_string(length=7)
                        new_top.createdDate = datetime.datetime.now()
                        new_top.creator = request.user
                        new_top.save()
                        messages.success(request, "Alt kategori başarıyla eklendi.")
                        return redirect("admin_add_article_category")
                    else:
                        title = request.POST.get('title')
                        isActive = request.POST.get("isActive") == 'on'
                        new_lower = ArticleCategory(title=title, isCategory=True, isActive=isActive, isRoot=False, parentId=inputTop)
                        new_lower.catNumber = "c-" + get_random_string(length=7)
                        new_lower.createdDate = datetime.datetime.now()
                        new_lower.creator = request.user
                        new_lower.save()
                        messages.success(request, "En alt kategori başarıyla eklendi.")
                        return redirect("admin_add_article_category")
                return render(request, "adminpanel/article/add-category.html", context)
            else:
                inputTop = ArticleCategory.objects.get(catNumber=getTop)
                selectSub = ArticleCategory.objects.filter(parentId=inputTop)
                context = {
                    "getTop": getTop,
                    "inputTop": inputTop,
                    "selectSub": selectSub,
                    "userGroup": userGroup,
                }
                return render(request, "adminpanel/article/add-category.html", context)
        else:
            return render(request, "adminpanel/article/add-category.html", context)
    else:
        return redirect("index")



# instance.catNumber = "c-" + get_random_string(length=6)

@login_required(login_url="login_admin")
def admin_edit_article_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=True)).order_by('title')
    userGroup = current_user_group(request, request.user)
    try:
        instance = ArticleCategory.objects.get(slug=slug)
        if userGroup == 'admin' or userGroup == "moderator":
            if request.method == "POST":
                value = request.POST['categoryId']
                title = request.POST.get("title")
                isActive = request.POST.get("isActive") == "on"
                isCategory = request.POST.get("isCategory") == "on"
                if instance.parentId_id != value:
                    instance.parentId_id = value
                    instance.title = title
                    instance.isActive = isActive
                    instance.isCategory = isCategory
                    pre_save.connect(slug_save, sender=ArticleCategory)
                    instance.save()
                    messages.success(request, "Makale kategorisi başarıyla güncellendi.")
                    return redirect("admin_article_categories")
                messages.error(request, "Eklemek istediğiniz kategori zaten mevcut.")
                return redirect("admin_article_categories")
            context = {
                "userGroup": userGroup,
                "articleCategory": articleCategory,
                "instance": instance,
            }
            return render(request, "adminpanel/article/edit-category.html", context)
    except:
        messages.error(request, "Makale kategorisi bulunamadı.")
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
    form = EditArticleForm(request.POST or None, instance=instance)
    context = {
        "articleCategory": articleCategory,
        "userGroup": userGroup,
        "form": form,
        "instance": instance,
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
        instance.isPrivate = isPrivate
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
        return redirect("admin_all_articles")
    return render(request, "adminpanel/article/edit-article.html", context)


@login_required(login_url="login_admin")
def admin_article_categories(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = ArticleCategory.objects.filter(isActive=True)
    context = {
        "categories": categories,
        "userGroup": userGroup,
    }
    return render(request, "adminpanel/article/categories.html", context)


@login_required(login_url="login_admin")
def admin_isactive_article_category(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    try:
        instance = ArticleCategory.objects.get(slug=slug)
        if userGroup == 'admin':
            if instance.isActive is True:
                instance.isActive = False
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Makale kategorisi artık aktif değil.")
                return redirect("admin_article_categories")
            else:
                instance.isActive = True
                instance.updatedDate = datetime.datetime.now()
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
    """
    :param request:
    :param slug:
    :return:
    """
    instance = get_object_or_404(ArticleCategory, slug=slug)
    if instance.isActive is True:
        messages.error(request, "Makale kategorisi aktif olduğu için silme işlemi gerçekleştirilemedi.")
        return redirect("admin_article_categories")
    else:
        instance.delete()
        messages.success(request, "Makale kategorisi başarıyla silindi.")
        return redirect("admin_article_categories")


class ArticleCategoryView(DetailView):

    @staticmethod
    @login_required(login_url="login_admin")
    def getTopCategory(request):
        """
        :param request:
        :return topCategory:
        """
        topCategory = ArticleCategory.objects.filter(Q(isActive=True, isRoot=False, parentId__slug="home", isCategory=True)|Q(isRoot=True))
        return topCategory

    @staticmethod
    @login_required(login_url="login_admin")
    def getSubCategory(request, catNumber):
        """
        :param request:
        :param catNumber:
        :return subCategory:
        """
        instance = get_object_or_404(ArticleCategory, catNumber=catNumber)
        subCategory = ArticleCategory.objects.filter(parentId__catNumber=instance)
        return subCategory

    @staticmethod
    @login_required(login_url="login_admin")
    def getLowCategory(request, catNumber):
        """
        :param request:
        :return catNumber:
        """
        instance = get_object_or_404(ArticleCategory, catNumber=catNumber)
        lowCategory = ArticleCategory.objects.filter(parentId__catNumber=instance.catNumber)
        return lowCategory

