from ckeditor.widgets import CKEditorWidget
from django import forms

from article.models import Article


class ArticleForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget(), label="Yazı")
    abstract = forms.CharField(widget=CKEditorWidget(), label="Abstract")


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['abstract', 'description', 'media']
