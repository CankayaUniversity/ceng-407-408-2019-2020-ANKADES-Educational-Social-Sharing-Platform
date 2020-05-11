from rest_framework import serializers

from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['postNumber', 'title', 'slug', 'createdDate', 'updatedDate', 'view', 'isActive', 'media', 'description']
        lookup_field = 'postNumber'