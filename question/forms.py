from ckeditor.widgets import CKEditorWidget
from django import forms


class AddQuestionForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget())
