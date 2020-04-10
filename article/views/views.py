import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.db.models.signals import pre_save
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import RedirectView
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from account.models import AccountLogs
from account.views.views import current_user_group
from ankadescankaya.slug import slug_save
from article.forms import EditArticleForm, ArticleForm
from article.models import Article, ArticleCategory, ArticleComment
from article.serializers import ArticleCategorySerializer, ArticleCommentSerializer, ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleCommentViewSet(viewsets.ModelViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer


class ArticleCategoryViewSet(viewsets.ModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer


def all_articles(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articles_categories_lists = ArticleCategory.objects.all()
    articles_limit = Article.objects.all().order_by('-createdDate')
    articleComment = ArticleComment.objects.all()
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        context = {
            "articles": articles,
            "articles_categories_lists": articles_categories_lists,
            "articles_limit": articles_limit,
            "currentUser": currentUser,
            "userGroup": userGroup,
        }
        return render(request, "ankades/article/all-articles.html", context)
    else:
        articles = Article.objects.filter(isActive=True)
        paginator = Paginator(articles, 12)
        try:
            article_pagination = paginator.page(page)
        except PageNotAnInteger:
            article_pagination = paginator.page(1)
        except EmptyPage:
            article_pagination = paginator.page(paginator.num_pages)
        context = {
            "articles": articles,
            "articleComment": articleComment,
            "article_pagination": article_pagination,
            "articles_categories_lists": articles_categories_lists,
            "articles_limit": articles_limit,
            "currentUser": currentUser,
            "userGroup": userGroup,
        }
        return render(request, "ankades/article/all-articles.html", context)


@login_required(login_url="login_admin")
def article_categories(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=True))
    categories = ArticleCategory.objects.all()
    article_categories_limit = ArticleCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "article_categories_limit": article_categories_limit,
        "currentUser": currentUser,
        "articleCategory": articleCategory,
    }
    return render(request, "adminpanel/article/categories.html", context)


@login_required(login_url="login_account")
def add_article(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    form = ArticleForm(request.POST or None)
    activity = AccountLogs()
    context = {
        "articleCategory": articleCategory,
        "userGroup": userGroup,
        "form": form,
        "currentUser": currentUser,
    }
    if request.method == "POST":
        value = request.POST['categoryId']
        title = request.POST.get("title")
        isPrivate = request.POST.get("isPrivate") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
        if not title and description:
            messages.error(request, "Kategori, Başlık ve Açıklama kısımları boş geçilemez")
            return render(request, "ankades/article/add-article.html", context)
        instance = Article(title=title, description=description, isPrivate=isPrivate)
        if request.FILES:
            media = request.FILES.get('media')
            fs = FileSystemStorage()
            fs.save(media.name, media)
            instance.media = media
        instance.creator = currentUser
        instance.categoryId_id = value
        instance.isActive = True
        instance.save()
        activity.title = "Makale Ekle"
        activity.application = "Article"
        activity.method = "POST"
        activity.creator = currentUser
        activity.createdDate = datetime.datetime.now()
        activity.description = str(activity.createdDate) + " tarihinde, " + str(
            activity.creator) + " kullanıcısı makale ekledi."
        activity.save()
        messages.success(request, "Makale başarıyla eklendi !")
        return redirect("index")
    return render(request, "ankades/article/add-article.html", context)


@login_required(login_url="login_admin")
def edit_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    activity = AccountLogs()
    try:
        instance = Article.objects.get(slug=slug)
        form = EditArticleForm(request.POST or None, instance=instance)
        description = instance.description
        if instance.creator == currentUser:
            if request.method == "POST":
                value = request.POST['id']
                title = request.POST.get("title")
                isPrivate = request.POST.get("isPrivate") == "on"
                if form.is_valid():
                    description = form.cleaned_data.get("description")
                if request.FILES:
                    media = request.FILES.get('media')
                    fs = FileSystemStorage()
                    fs.save(media.name, media)
                    instance.media = media
                instance.title = title
                instance.isPrivate = isPrivate
                instance.description = description
                instance.creator = request.user
                instance.categoryId_id = value
                instance.updatedDate = datetime.datetime.now()
                instance.isActive = False
                instance.save()
                activity.title = "Makale Güncelleme"
                activity.application = "Article"
                activity.createdDate = datetime.datetime.now()
                activity.method = "UPDATE"
                activity.creator = currentUser
                activity.description = str(activity.createdDate) + " tarihinde, " + str(
                    activity.creator) + " kullanıcısı makalesini güncelledi."
                activity.save()
                pre_save.connect(slug_save, sender=edit_article)
                messages.success(request, "Makale başarıyla güncellendi.")
                return redirect(reverse("article_detail", kwargs={"username": instance.creator, "slug": slug}))
            context = {
                "instance": instance,
                "articleCategory": articleCategory,
                "userGroup": userGroup,
                "form": form,
                "currentUser": currentUser,
            }
            return render(request, "ankades/account/posts/edit-article.html", context)
    except:
        return render(request, "404.html")


def article_categories(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    keyword = request.GET.get("keyword")
    if keyword:
        searchCategories = ArticleCategory.objects.filter(title__contains=keyword)
        context = {
            "searchCategories": searchCategories,
            "userGroup": userGroup,
            "currentUser": currentUser,
        }
        return render(request, "ankades/article/categories.html", context)
    categories = ArticleCategory.objects.all()
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "currentUser": currentUser,
    }
    return render(request, "ankades/article/categories.html", context)


def article_detail(request, username, slug):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    try:
        instance = Article.objects.get(slug=slug)
        if instance.creator.username != username:
            messages.error(request, "Aradığınız makale ile kullanıcı eşleştirilemedi.")
            return render(request, "404.html")
        articles = Article.objects.all()
        relatedPosts = Article.objects.all().order_by('-createdDate')[:5]
        articleComments = ArticleComment.objects.filter(articleId__slug=slug)
        articleCategories = ArticleCategory.objects.all()
        instance.view += 1
        instance.save()
        context = {
            "articles": articles,
            "relatedPosts": relatedPosts,
            "articleComments": articleComments,
            "articleCategories": articleCategories,
            "instance": instance,
            "currentUser": currentUser,
            "userGroup": userGroup,
        }
        return render(request, "ankades/article/article-detail.html", context)
    except:
        return render(request, "404.html")


@login_required(login_url="login_account")
def delete_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    currentUser = request.user
    if instance.creator == currentUser:
        if instance.isActive:
            instance.isActive = False
            messages.success(request, "Makale başarıyla silindi.")
            return redirect(reverse("account_detail", kwargs={"username": currentUser}))
    else:
        messages.error(request, "Bu makale size ait değil")
        return redirect(reverse("account_detail", kwargs={"username": currentUser}))


@login_required(login_url="login_account")
def add_article_comment(request, slug):
    currentUser = request.user
    activity = AccountLogs()
    activity.application = "Article"
    activity.creator = currentUser
    activity.createdDate = datetime.datetime.now()
    activity.title = "Makale Yorumu Ekle"
    instance = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        content = request.POST.get("content")
        new_comment = ArticleComment(content=content, creator=request.user)
        new_comment.articleId = instance
        new_comment.save()
        activity.description = "Makaleye yeni bir yorum eklendi. İşlemi yapan kişi: " + str(
            activity.creator) + ". İşlemin gerçekleştirildiği tarih: " + str(activity.createdDate)
        activity.save()
        messages.success(request, "Makale yorumu başarıyla oluşturuldu.")
    return redirect("all_articles")


def get_article_categories(request):
    articleCategory = ArticleCategory.objects.filter(isRoot=False)
    return None


class ArticleLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Article, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_