from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import Q

from article.models import Article, ArticleCategory


class ArticleForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget(), label="Yazı")
    isPrivate = forms.BooleanField(widget=forms.Select(attrs={'class': 'custom-control-input'}), label="Özel")


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['categoryId', 'title', 'description', 'isPrivate', 'isActive', 'media']
