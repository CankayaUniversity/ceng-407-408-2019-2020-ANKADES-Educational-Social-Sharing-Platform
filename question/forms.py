from ckeditor.widgets import CKEditorWidget
from django import forms


class AddQuestionForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
