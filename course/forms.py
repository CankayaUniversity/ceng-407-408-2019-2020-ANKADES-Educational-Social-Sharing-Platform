from ckeditor.widgets import CKEditorWidget
from django import forms

from article.models import ArticleComment


class AddArticleComment(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['content', ]


class CourseForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget(), label="Yazı")