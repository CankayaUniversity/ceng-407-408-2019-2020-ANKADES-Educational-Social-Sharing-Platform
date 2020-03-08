from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import Q
from adminpanel.models import Tag
from article.models import ArticleCategory


class ArticleForm(forms.Form):
    categoryId = forms.ModelChoiceField(
        queryset=ArticleCategory.objects.filter(Q(isRoot=False), Q(isActive=True), Q(isCategory=False)),
        label="Kategori Adı")
    tagId = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(isActive=True), label="Etiket", required=False)
    title = forms.CharField(max_length=None, label="Başlık")
    description = forms.CharField(widget=CKEditorWidget(), label="Yazı")
    isPrivate = forms.BooleanField(required=False, label="Özel olacak ise kutucuğu işaretleyin")
    media = forms.FileField(allow_empty_file=True, required=False, label="Dosya")
