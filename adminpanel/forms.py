from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import Q
from account.models import Group
from course.models import CourseCategory


class AdminEditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'isActive']


class ArticleForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget())


class SiteSettingsForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget())


class QuestionForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget())
