from django import forms


# Users
from account.models import Account


class AccountRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50, label="Kullanıcı Adı")
    email = forms.EmailField(label="Email Adresi")
    password = forms.CharField(min_length=6, max_length=50, label="Şifre", widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=6, max_length=50, label="Şifre Tekrar", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Girilen şifreler uyuşmuyor! Lütfen tekrar deneyin.")

        values = {
            "username": username,
            "email": email,
            "password": password,
            # "captcha": captcha,
        }
        return values


class AccountLoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        values = {
            "username": username,
            "password": password
        }
        return values


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["username", "first_name", "last_name", "email", "image", "description"]
        help_texts = {
            'username': None,
            'first_name': None,
            'last_name': None,
            'email': None,
            'description': None
        }

