from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import Q

from article.models import Article, ArticleCategory


class ArticleForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget(), label="Yazı")


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['description', 'isPrivate']
