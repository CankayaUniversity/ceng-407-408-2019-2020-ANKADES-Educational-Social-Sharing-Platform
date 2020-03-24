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
from account.models import Account, AccountActivity
from account.views.views import current_user_group
from adminpanel.forms import AddArticleForm
from ankadescankaya.slug import slug_save
from article.forms import ArticleForm, EditArticleForm
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
    articles_categories_lists = ArticleCategory.objects.all()
    articles_limit = Article.objects.all().order_by('-createdDate')[:5]
    articleComment = ArticleComment.objects.all()
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        context = {
            "articles": articles,
            "articles_categories_lists": articles_categories_lists,
            "articles_limit": articles_limit,
        }
        return render(request, "ankades/../templates/test/article/articles.html", context)
    else:
        articles = Article.objects.all()
        paginator = Paginator(articles, 1)
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
        }
        return render(request, "ankades/../templates/test/article/articles.html", context)


@login_required(login_url="login_admin")
def article_categories(request):
    """
    :param request:
    :return:
    """
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    categories = ArticleCategory.objects.all()
    article_categories_limit = ArticleCategory.objects.all().order_by('-createdDate')[:5]
    context = {
        "categories": categories,
        "userGroup": userGroup,
        "article_categories_limit": article_categories_limit,
        "currentUser": currentUser,
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
    form = AddArticleForm(request.POST or None)
    context = {
        "articleCategory": articleCategory,
        "userGroup": userGroup,
        "form": form,
    }
    if request.method == "POST":
        value = request.POST['categoryId']
        title = request.POST.get("title")
        if form.is_valid():
            description = form.cleaned_data.get("description")
        isPrivate = request.POST.get("isPrivate") == "on"
        isActive = request.POST.get("isActive") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
        if not title and description:
            messages.error(request, "Kategori, Başlık ve Açıklama kısımları boş geçilemez")
            return render(request, "ankades/article/add-article.html", context)
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
    instance = get_object_or_404(Article, slug=slug)
    activity = AccountActivity()
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
            # return redirect(reverse("article_detail", kwargs={"slug": slug}))
            return redirect("index")
        context = {
            "instance": instance,
            "articleCategory": articleCategory,
            "userGroup": userGroup,
            "form": form,
        }
        return render(request, "ankades/account/posts/edit-article.html", context)


def article_categories(request):
    keyword = request.GET.get("keyword")
    if keyword:
        searchCategories = ArticleCategory.objects.filter(title__contains=keyword)
        return render(request, "ankades/article/categories.html", {"searchCategories": searchCategories})
    categories = ArticleCategory.objects.all()
    return render(request, "ankades/article/categories.html", {"categories": categories})


def article_detail(request, username, slug):
    instance = get_object_or_404(Article, slug=slug)
    if instance.creator.username != username:
        messages.error(request, "Aradığınız şeyi bulamadık")
        return redirect("index")
    articles = Article.objects.all()
    relatedPosts = Article.objects.all().order_by('-createdDate')[:4]
    articleComments = ArticleComment.objects.filter(articleId__slug=slug)
    articleCategories = ArticleCategory.objects.all()
    instance.view += 1
    context = {
        "articles": articles,
        "relatedPosts": relatedPosts,
        "articleComments": articleComments,
        "articleCategories": articleCategories,
        "instance": instance,
        "title": instance.title,
        "description": instance.description,
        "media": instance.media
    }
    return render(request, "ankades/article/article-detail.html", context)


@login_required(login_url="login_account")
def delete_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    instance.delete()
    messages.success(request, "Makale başarıyla silindi.")
    return redirect("user_posts")


@login_required(login_url="login_account")
def my_articles(request, username):
    keyword = request.GET.get("keyword")
    if keyword:
        article_pagination = Article.objects.filter(Q(title__contains=keyword) |
                                                    Q(description__contains=keyword))
        context = {
            "article_pagination": article_pagination,
        }
        return render(request, "ankades/../templates/test/article/my-articles.html", context)
    user = get_object_or_404(Account, username=username)
    articleCategories = Article.objects.all()
    myArticles = Article.objects.filter(Q(creator=user))
    context = {
        "myArticles": myArticles,
        "articleCategories": articleCategories,
    }
    return render(request, "ankades/../templates/test/article/my-articles.html", context)


@login_required(login_url="login_account")
def add_article_comment(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        content = request.POST.get("content")
        new_comment = ArticleComment(content=content, creator=request.user)
        new_comment.articleId = instance
        new_comment.save()
    return redirect(reverse("article_detail", kwargs={"slug": slug}))


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