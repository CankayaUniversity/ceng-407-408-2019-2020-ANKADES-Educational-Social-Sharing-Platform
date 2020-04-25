import uuid

from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models.signals import pre_save
from rest_framework.reverse import reverse

from account.models import Account
from adminpanel.models import Tag
from ankadescankaya.slug import slug_save
from ankadescankaya.storage_backends import ArticleMediaStorage


class ArticleCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = models.TextField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    isRoot = models.BooleanField(default=False)
    tree = ArrayField(JSONField(default=dict), max_length=200, blank=True, default=list)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isCategory = models.BooleanField(default=False)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = "ArticleCategory"
        ordering = ['-createdDate']


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, null=False)
    postNumber = models.CharField(unique=True, null=True, blank=True, max_length=32)
    title = models.CharField(max_length=254, null=False, blank=False)
    slug = models.SlugField(unique=True, max_length=254, allow_unicode=True)
    description = RichTextField(null=False, blank=False)
    media = models.FileField(null=True, blank=True, storage=ArticleMediaStorage(), default="no-image-available.png")
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isPrivate = models.BooleanField(default=False, null=True, blank=True)
    likes = models.ManyToManyField(Account, related_name="articleLikes", default=0, blank=True,
                                   db_table="AccountLikedArticle")
    readTime = models.IntegerField(default=0)
    introduction = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"username": self.creator, "slug": self.slug})

    def get_like_url(self):
        return reverse("article-like-toggle", kwargs={"username": self.creator, "slug": self.slug})

    def get_api_like_url(self):
        return reverse("article-like-api-toggle", kwargs={"username": self.creator, "slug": self.slug})

    class Meta:
        db_table = "Article"
        ordering = ['-createdDate']


class ArticleComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    articleId = models.ForeignKey(Article, on_delete=models.CASCADE)
    commentNumber = models.CharField(unique=True, null=False, blank=False, max_length=32)
    creator = models.ForeignKey(Account, max_length=50, on_delete=models.CASCADE)
    content = RichTextField(blank=False, null=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(null=True, blank=True)
    parentId = models.ForeignKey('self', null=True, related_name="articleCommentId", on_delete=models.CASCADE)
    isRoot = models.BooleanField(default=False)
    isReply = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.creator

    class Meta:
        db_table = "ArticleComment"
        ordering = ['-createdDate']


class ArticleTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tagId = models.ForeignKey(Tag, on_delete=models.CASCADE)
    articleId = models.ForeignKey(Article, on_delete=models.CASCADE)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = "ArticleTag"


pre_save.connect(slug_save, sender=Article)
pre_save.connect(slug_save, sender=ArticleCategory)
