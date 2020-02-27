from django.contrib.auth.models import User
from rest_framework import serializers

from article.models import Article, ArticleComment, ArticleCategory


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'description', 'creator', 'categoryId', 'media', 'createdDate', 'updatedDate', 'view', 'isActive', 'like']


class ArticleCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['articleId', 'creator', 'content', 'createdDate', 'updatedDate', 'parentId', 'isRoot', 'isActive', 'view', 'like']


class ArticleCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ['creator', 'title', 'slug', 'description', 'createdDate', 'updatedDate', 'parentId', 'isRoot', 'view', 'isActive']