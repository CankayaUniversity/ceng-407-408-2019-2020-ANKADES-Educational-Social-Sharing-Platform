from rest_framework import serializers

from article.models import Article
from question.models import Question


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['postNumber', 'title']
        lookup_field = 'postNumber'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'