import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.db.models.signals import pre_save
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import RedirectView
from rest_framework import viewsets

from ankadescankaya.slug import slug_save
from ankadescankaya.views import Categories
from ankadescankaya.views import current_user_group
from article.forms import EditArticleForm, ArticleForm
from article.models import Article, ArticleCategory, ArticleComment
from article.serializers import ArticleCategorySerializer, ArticleCommentSerializer, ArticleSerializer
from support.models import Report


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
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    articles_categories_lists = ArticleCategory.objects.filter(isActive=True)
    articles_limit = Article.objects.filter(isActive=True).order_by('-createdDate')
    articleComment = ArticleComment.objects.filter(isActive=True)
    page = request.GET.get('page', 1)
    keyword = request.GET.get("keyword")
    categories = Categories.all_categories()
    if keyword:
        articles = Article.objects.filter(Q(title__contains=keyword, isActive=True)).order_by('-createdDate')
        context = {
            "articles": articles,
            "articles_categories_lists": articles_categories_lists,
            "articles_limit": articles_limit,
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/article/all-articles.html", context)
    else:
        articles = Article.objects.filter(isActive=True).order_by('-createdDate')
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
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/article/all-articles.html", context)


def article_category_page(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        articleCategory = ArticleCategory.objects.get(slug=slug)
        articles = Article.objects.filter(categoryId=articleCategory)
        context = {
            "articleCategory": articleCategory,
            "articles": articles,
            "userGroup": userGroup,
            "articleCategories": categories[0],
            "articleSubCategories": categories[1],
            "articleLowerCategories": categories[2],
            "questionCategories": categories[3],
            "questionSubCategories": categories[4],
            "questionLowerCategories": categories[5],
            "courseCategories": categories[6],
            "courseSubCategories": categories[7],
            "courseLowerCategories": categories[8],
        }
        return render(request, "ankades/article/get-article-category.html", context)
    except:
        return redirect("404")


@login_required(login_url="login_account")
def add_article(request):
    """
    :param request:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    form = ArticleForm(request.POST or None)
    categories = Categories.all_categories()
    context = {
        "articleCategory": articleCategory,
        "userGroup": userGroup,
        "form": form,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
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
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    articleCategory = ArticleCategory.objects.filter(Q(isActive=True, isCategory=False))
    try:
        instance = Article.objects.get(slug=slug)
        form = EditArticleForm(request.POST or None, instance=instance)
        description = instance.description
        if instance.creator == request.user:
            if request.method == "POST":
                value = request.POST['id']
                title = request.POST.get("title")
                isPrivate = request.POST.get("isPrivate") == "on"
                if form.is_valid():
                    description = form.cleaned_data.get("description")
                if request.FILES:
                    if instance.media:
                        instance.media = None
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
                pre_save.connect(slug_save, sender=edit_article)
                messages.success(request, "Makale başarıyla güncellendi.")
                return redirect(reverse("article_detail", kwargs={"username": instance.creator, "slug": slug}))
            context = {
                "instance": instance,
                "articleCategory": articleCategory,
                "userGroup": userGroup,
                "form": form,
                "articleCategories": categories[0],
                "articleSubCategories": categories[1],
                "articleLowerCategories": categories[2],
                "questionCategories": categories[3],
                "questionSubCategories": categories[4],
                "questionLowerCategories": categories[5],
                "courseCategories": categories[6],
                "courseSubCategories": categories[7],
                "courseLowerCategories": categories[8],
            }
            return render(request, "ankades/account/posts/edit-article.html", context)
    except:
        return redirect("404")


def article_detail(request, username, slug):
    """
    :param request:
    :param username:
    :param slug:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    try:
        instance = Article.objects.get(slug=slug)
    except:
        return redirect("404")
    if instance.creator.username != username:
        return render(request, "404.html")
    articles = Article.objects.filter(isActive=True)
    relatedPosts = Article.objects.filter(isActive=True).order_by('-createdDate')[:5]
    articleComments = ArticleComment.objects.filter(articleId__slug=slug, isRoot=True, isActive=True)
    replyComment = ArticleComment.objects.filter(isReply=True, isRoot=False, isActive=True)
    instance.view += 1
    instance.save()
    context = {
        "articles": articles,
        "relatedPosts": relatedPosts,
        "instance": instance,
        "userGroup": userGroup,
        "articleComments": articleComments,
        "replyComment": replyComment,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    return render(request, "ankades/article/article-detail.html", context)


@login_required(login_url="login_account")
def add_report_article(request, postNumber):
    """
    :param postNumber:
    :param request:
    :return:
    """
    try:
        instance = Article.objects.get(postNumber=postNumber)
        if request.method == "POST":
            description = request.POST.get("description")
            new_report = Report(description=description, isActive=True, isSolved=False, isRead=False, createdDate=datetime.datetime.now())
            new_report.creator = request.user
            new_report.supportNumber = get_random_string(length=32)
            new_report.title = "Kullanıcı Şikayeti"
            new_report.post = postNumber
            new_report.displayMessage = str(new_report.creator.get_full_name()) + " adlı kullanıcı makale için şikayette bulundu. Makale numarası: " + postNumber
            new_report.save()
            messages.success(request, "Şikayetiniz başarıyla gönderildi. En kısa sürede tarafınıza geri dönüş sağlanacaktır.")
            return redirect(reverse("article_detail", kwargs={"username": instance.creator, "slug": instance.slug}))
        return redirect(reverse("article_detail", kwargs={"username": instance.creator, "slug": instance.slug}))
    except:
        messages.error(request, "Makale bulunamadı.")
        return redirect("404")


@login_required(login_url="login_account")
def delete_article(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        instance = Article.objects.get(slug=slug)
        request.user = request.user
        if instance.creator == request.user:
            if instance.isActive:
                instance.isActive = False
                instance.save()
                messages.success(request, "Makale başarıyla silindi.")
                return redirect(reverse("account_detail", kwargs={"username": request.user}))
            else:
                return redirect(reverse("account_detail", kwargs={"username": request.user}))
        else:
            return redirect("404")
    except:
        return redirect("404")


@login_required(login_url="login_account")
def add_article_comment(request, slug):
    """
    :param request:
    :param slug:
    :return:
    """
    request.user = request.user
    try:
        instance = Article.objects.get(slug=slug)
        if request.method == "POST":
            content = request.POST.get("content")
            new_comment = ArticleComment(content=content, creator=request.user)
            new_comment.articleId = instance
            new_comment.commentNumber = get_random_string(length=32)
            new_comment.isRoot = True
            new_comment.save()
            messages.success(request, "Makale yorumu başarıyla oluşturuldu.")
            return redirect(
                reverse("article_detail",
                        kwargs={"username": new_comment.articleId.creator, "slug": new_comment.articleId.slug}))
    except:
        return redirect("404")


@login_required(login_url="login_account")
def add_article_comment_reply(request, commentNumber):
    """
    :param request:
    :param commentNumber:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    try:
        instance = ArticleComment.objects.get(commentNumber=commentNumber)
        if request.method == "POST":
            reply = request.POST.get("reply")
            new_answer = ArticleComment(content=reply, creator=request.user)
            new_answer.articleId = instance.articleId
            new_answer.commentNumber = get_random_string(length=32)
            new_answer.parentId_id = instance.id
            new_answer.isActive = True
            new_answer.isRoot = False
            new_answer.isReply = True
            new_answer.save()
            messages.success(request, "Yorumunuz başarıyla oluşturuldu.")
        return redirect(
            reverse("article_detail",
                    kwargs={"username": instance.articleId.creator, "slug": instance.articleId.slug}), context)
    except:
        messages.error(request, "Makale bulunamadı.")
        return redirect("all_articles")


@login_required(login_url="login_account")
def edit_article_comment(request, commentNumber):
    """
    :param request:
    :param commentNumber:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    try:
        instance = ArticleComment.objects.get(commentNumber=commentNumber)
        article = Article.objects.get(slug=instance.articleId.slug)
        if request.method == "POST":
            edit = request.POST.get("edit")
            instance.content = edit
            instance.updatedDate = datetime.datetime.now()
            article.view -= 1
            article.save()
            instance.save()
            messages.success(request, "Yorumunuz başarıyla güncellendi.")
        return redirect(
            reverse("article_detail",
                    kwargs={"username": instance.articleId.creator, "slug": instance.articleId.slug}), context)
    except:
        messages.error(request, "Makale bulunamadı.")
        return redirect("all_articles")


@login_required(login_url="login_account")
def delete_article_comment(request, commentNumber):
    """
    :param request:
    :param commentNumber:
    :return:
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    context = {
        "userGroup": userGroup,
        "articleCategories": categories[0],
        "articleSubCategories": categories[1],
        "articleLowerCategories": categories[2],
        "questionCategories": categories[3],
        "questionSubCategories": categories[4],
        "questionLowerCategories": categories[5],
        "courseCategories": categories[6],
        "courseSubCategories": categories[7],
        "courseLowerCategories": categories[8],
    }
    try:
        instance = ArticleComment.objects.get(commentNumber=commentNumber)
        article = Article.objects.get(slug=instance.articleId.slug)
        instance.isActive = False
        instance.updatedDate = datetime.datetime.now()
        article.view -= 1
        article.save()
        instance.save()
        messages.success(request, "Yorum başarıyla silindi.")
        return redirect(
            reverse("article_detail",
                    kwargs={"username": instance.articleId.creator, "slug": instance.articleId.slug}), context)
    except:
        messages.error(request, "Makale bulunamadı.")
        return redirect("all_articles")


class ArticleLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        slug = self.kwargs.get("slug")
        try:
            obj = Article.objects.get(slug=slug)
            url_ = obj.get_absolute_url()
            user = self.request.user
            if user.is_authenticated:
                if user in obj.likes.all():
                    obj.likes.remove(user)
                else:
                    obj.likes.add(user)
            return url_
        except:
            return redirect("404")
