from django import forms

from article.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["media", "title", "slug", "categoryId", "description"]
