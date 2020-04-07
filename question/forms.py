from ckeditor.widgets import CKEditorWidget
from django import forms

from question.models import Question


class QuestionForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget())


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['description',]