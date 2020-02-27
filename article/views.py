from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from account.models import Group, AccountGroup
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
    keyword = request.GET.get("keyword")
    if keyword:
        article_pagination = Article.objects.filter(Q(article_title__contains=keyword) |
                                                    Q(article_content__contains=keyword))
        context = {
            "article_pagination": article_pagination,
        }
        return render(request, "ankades/article/articles.html", context)

    articles = Article.objects.all()
    articles_limit = Article.objects.all().order_by('-id')[:10]
    articles_categories_lists = ArticleCategory.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        article_pagination = paginator.page(page)
    except PageNotAnInteger:
        article_pagination = paginator.page(1)
    except EmptyPage:
        article_pagination = paginator.page(paginator.num_pages)

    context = {
        "articles": articles,
        "article_pagination": article_pagination,
        "articles_categories_lists": articles_categories_lists,
        "articles_limit": articles_limit,
    }
    return render(request, "ankades/article/articles.html", context)


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


# @login_required(login_url="user:login")
# def add_article_comment(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     articleCommet = ArticleComment.objects.get(articleId__slug=slug)
#     if request.method == "POST":
#          = request.POST.get("article_comment_author")
#         article_comment_content = request.POST.get("article_comment_content")
#
#         new_comment = ArticleComment(article_comment_author=article_comment_author,
#                                      article_comment_content=article_comment_content)
#         new_comment.article_comment = article
#         new_comment.save()
#     # return redirect(reverse("article:article_detail", kwargs={"id": id}))
#     return render(request, "ankades/article/article-detail.html")