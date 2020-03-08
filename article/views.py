import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from account.models import AccountGroup, Account
from article.forms import ArticleForm, EditArticleForm
from article.models import Article, ArticleCategory, ArticleComment, ArticleTag
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
    article_tags = ArticleTag.objects.all().order_by('-createdDate')[:5]
    articles_categories_lists = ArticleCategory.objects.all()
    articles_limit = Article.objects.all().order_by('-createdDate')[:5]
    articleComment = ArticleComment.objects.all()
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        context = {
            "articles": articles,
            "article_tags": article_tags,
            "articles_categories_lists": articles_categories_lists,
            "articles_limit": articles_limit,
        }
        return render(request, "ankades/article/articles.html", context)
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
            "article_tags": article_tags,
            "articles_categories_lists": articles_categories_lists,
            "articles_limit": articles_limit,
        }
        return render(request, "ankades/article/articles.html", context)


@login_required(login_url="login_account")
def add_article(request):
    """
    :param request:
    :return:
    """
    form = ArticleForm(request.POST or None)
    context = {
        "form": form
    }
    adminGroup = AccountGroup.objects.filter(
        Q(userId__username=request.user.username, groupId__slug="admin") |
        Q(userId__username=request.user.username, groupId__slug="moderator") |
        Q(userId__username=request.user.username, groupId__slug="ogretmen"))
    if adminGroup:
        if form.is_valid():
            categoryId = form.cleaned_data.get("categoryId")
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            isActive = form.cleaned_data.get("isActive")
            isPrivate = form.cleaned_data.get("isPrivate")
            media = form.cleaned_data.get("media")
            instance = Article(categoryId=categoryId, title=title, description=description, isActive=isActive,
                               isPrivate=isPrivate, media=media)
            instance.creator = request.user
            instance.save()
            messages.success(request, "Makale başarıyla eklendi !")
            return redirect("my_articles")
        return render(request, "ankades/article/add-article.html", context)
    else:
        messages.error(request, "Yetkiniz yok!")
        return redirect("index")


@login_required(login_url="login_admin")
def edit_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    accountGroup = AccountGroup.objects.filter(
        Q(userId__username=request.user.username, groupId__slug="admin") |
        Q(userId__username=request.user.username, groupId__slug="moderator") |
        Q(userId__username=request.user.username, groupId__slug="ogretmen"))
    currentUser = request.user.username
    instance = get_object_or_404(Article, slug=slug)
    if accountGroup:
        if instance.creator.username == currentUser:
            form = EditArticleForm(request.POST or None, request.FILES or None, instance=instance)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.creator = request.user
                instance.updatedDate = datetime.datetime.now()
                instance.save()
                messages.success(request, "Makale başarıyla düzenlendi !")
                context = {
                    "form": form,
                }
                return render(request, "ankades/article/edit-article.html", context)
            return render(request, "ankades/article/edit-article.html", {"form": form})
        else:
            messages.error(request, "Sizin makaleniz değil")
            return redirect("index")
    else:
        messages.error(request, "Yetkiniz yok")
        return redirect("index")

def article_categories(request):
    keyword = request.GET.get("keyword")
    if keyword:
        searchCategories = ArticleCategory.objects.filter(title__contains=keyword)
        return render(request, "ankades/article/articles.html", {"searchCategories": searchCategories})
    categories = ArticleCategory.objects.all()
    return render(request, "ankades/article/articles.html", {"categories": categories})


def article_detail(request, slug):
    articleDetail = get_object_or_404(Article, slug=slug)
    articles = Article.objects.all()
    accountGroup = AccountGroup.objects.get(userId__article__slug=slug)
    articleComments = ArticleComment.objects.all()
    articleCategories = ArticleCategory.objects.all()
    articleDetail.view += 1
    context = {
        "articleDetail": articleDetail,
        "articles": articles,
        "accountGroup": accountGroup,
        "articleComments": articleComments,
        "articleCategories": articleCategories,
    }
    return render(request, "ankades/article/article-detail.html", context)


@login_required(login_url="login_account")
def delete_article(request, slug):
    instance = get_object_or_404(Article, slug=slug)
    if instance.isActive == True:
        instance.isActive = False
        instance.save()
        messages.success(request, "Makale başarıyla silindi.")
        return redirect("my_articles")
    else:
        messages.error(request, "Makale zaten silinmiş.")
        return redirect(my_articles)


@login_required(login_url="login_account")
def my_articles(request, username):
    keyword = request.GET.get("keyword")
    if keyword:
        article_pagination = Article.objects.filter(Q(title__contains=keyword) |
                                                    Q(description__contains=keyword))
        context = {
            "article_pagination": article_pagination,
        }
        return render(request, "ankades/article/my-articles.html", context)
    user = get_object_or_404(Account, username=username)
    articleCategories = Article.objects.all()
    myArticles = Article.objects.filter(Q(creator=user))
    context = {
        "myArticles": myArticles,
        "articleCategories": articleCategories,
    }
    return render(request, "ankades/article/my-articles.html", context)
