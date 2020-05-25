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

from account.views.views import get_user_follower
from adminpanel.views.article import ArticleCategoryView
from ankadescankaya.slug import slug_save
from ankadescankaya.views.views import current_user_group, Categories
from article.forms import ArticleForm, EditArticleForm
from article.models import Article, ArticleCategory, ArticleComment
from article.serializers import ArticleCategorySerializer, ArticleCommentSerializer, ArticleSerializer
from support.models import Report, ReportSubject


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
    """
    userGroup = current_user_group(request, request.user)
    categories = Categories.all_categories()
    category = request.GET.getlist('c')
    sub = request.GET.getlist('s')
    lower = request.GET.getlist('l')
    getLowCategory = []
    articleCat = []
    topCategories = ArticleCategoryView.getTopCategory(request)
    articleComment = ArticleComment.objects.filter(isActive=True)
    articles = Article.objects.filter(isActive=True)
    # TODO Paginator
    if category:
        top = ArticleCategory.objects.filter(catNumber__in=category)
        sub = ArticleCategory.objects.filter(isActive=True, parentId__catNumber__in=category)
        for getLower in sub:
            getLowCategory.append(getLower.catNumber)
        lower = ArticleCategory.objects.filter(isActive=True, parentId__catNumber__in=getLowCategory)
        for cat in lower:
            articleCat.append(cat.catNumber)
        articles = Article.objects.filter(isActive=True, categoryId__catNumber__in=articleCat)
        # TODO Paginator
        context = {
            "userGroup": userGroup,
            "articleComment": articleComment,
            "category": category,
            "sub": sub,
            "top": top,
            "articles": articles,
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
        return render(request, "ankacademy/article/all-articles.html", context)
    if sub:
        subCat = ArticleCategory.objects.filter(catNumber__in=sub)
        low = ArticleCategory.objects.filter(isActive=True, parentId__catNumber__in=sub)
        for getLower in low:
            getLowCategory.append(getLower.catNumber)
        articles = Article.objects.filter(isActive=True, categoryId__catNumber__in=getLowCategory)
        context = {
            "userGroup": userGroup,
            "articleComment": articleComment,
            "category": category,
            "low": low,
            "subCat": subCat,
            "sub": sub,
            "articles": articles,
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
        return render(request, "ankacademy/article/all-articles.html", context)
    if lower:
        lowCat = ArticleCategory.objects.filter(catNumber__in=lower)
        articles = Article.objects.filter(isActive=True, categoryId__catNumber__in=lower)
        context = {
            "userGroup": userGroup,
            "articleComment": articleComment,
            "lowCat": lowCat,
            "lower": lower,
            "articles": articles,
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
        return render(request, "ankacademy/article/all-articles.html", context)
    context = {
        "userGroup": userGroup,
        "topCategories": topCategories,
        "category": category,
        "articles": articles,
        "articleComment": articleComment,
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
    return render(request, "ankacademy/article/all-articles.html", context)


def article_category_page(request, catNumber):
    """
    :param request:
    :param slug:
    :return:
    """
    try:
        articleCategory = ArticleCategory.objects.get(catNumber=catNumber)
        articles = Article.objects.filter(categoryId=articleCategory)
        return articles
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
        value = request.POST['category']
        title = request.POST.get("title")
        owner = request.POST.get("owner")
        resource = request.POST.get("resource")
        introduction = request.POST.get("introduction")
        contact = request.POST.get("contact")
        isPrivate = request.POST.get("isPrivate") == "on"
        if form.is_valid():
            description = form.cleaned_data.get("description")
            abstract = form.cleaned_data.get("abstract")
        if not abstract or description:
            messages.error(request, "Makalenin hepsi veya ön yazısı yayınlanmadan devam edemezsiniz.")
            return render(request, "ankades/article/add-article.html", context)
        instance = Article(title=title, description=description, isPrivate=isPrivate, owner=owner, resource=resource)
        if request.FILES:
            media = request.FILES.get('media')
            instance.media = media
        instance.creator = request.user
        instance.categoryId_id = value
        instance.contact = contact
        instance.isActive = True
        instance.introduction = introduction
        instance.postNumber = get_random_string(length=32)
        instance.save()
        messages.success(request, "Makale başarıyla eklendi !")
        return redirect("index")
    return render(request, "ankacademy/article/add-article.html", context)


@login_required(login_url="login_account")
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
    except:
        return redirect("404")
    form = EditArticleForm(request.POST or None, instance=instance)
    description = instance.description
    if instance.creator == request.user or userGroup == 'admin' or userGroup == 'moderator':
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
    return redirect("index")


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
        creatorGroup = current_user_group(request, instance.creator)
        existFollower = get_user_follower(request, request.user, instance.creator)
    except:
        return redirect("404")
    if instance.creator.username != username:
        return render(request, "404.html")
    articles = Article.objects.filter(isActive=True)
    relatedPosts = Article.objects.filter(isActive=True).order_by('-createdDate')[:5]
    articleComments = ArticleComment.objects.filter(articleId__slug=slug, isRoot=True, isActive=True)
    replyComment = ArticleComment.objects.filter(isReply=True, isRoot=False, isActive=True)
    reportSubjects = ReportSubject.objects.filter(isActive=True)
    instance.view += 1
    instance.save()
    context = {
        "articles": articles,
        "creatorGroup": creatorGroup,
        "existFollower": existFollower,
        "reportSubjects": reportSubjects,
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
    return render(request, "ankacademy/article/article-detail.html", context)


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
            subjectId = request.POST['subjectId']
            description = request.POST.get("description")
            new_report = Report(subjectId_id=subjectId, description=description, isActive=True, isSolved=False, isRead=False, createdDate=datetime.datetime.now())
            new_report.creatorId = request.user
            new_report.reportNumber = get_random_string(length=32)
            new_report.title = "Kullanıcı Şikayeti"
            new_report.postNumber = postNumber
            new_report.displayMessage = str(new_report.creatorId.get_full_name()) + " adlı kullanıcı makale için şikayette bulundu. Makale numarası: " + postNumber
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
                    kwargs={"username": instance.articleId.creator, "slug": instance.articleId.slug}))
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
