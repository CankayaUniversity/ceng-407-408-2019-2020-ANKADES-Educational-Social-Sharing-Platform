from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms.widgets import TextInput


class MessageForm(forms.Form):
    message = forms.CharField(widget=TextInput(), label="Message")

    def clean(self):
        message = self.cleaned_data.get("message")

        values = {
            "message": message
        }
        return values