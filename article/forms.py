from ckeditor.fields import RichTextField
from django import forms

from adminpanel.models import Tag
from article.models import Article


# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ["media", "title", "slug", "categoryId", "description"]


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=None, label="Başlık")
    slug = forms.SlugField(max_length=None, label="Slug")
    tag = forms.ModelChoiceField(queryset=Tag.objects.filter(isActive=True), label="Etiket Seçin")
    description = RichTextField()
