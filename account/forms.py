from django import forms


# Users
class AccountRegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50, label="Kullanıcı Adı")
    email = forms.EmailField(label="Email Adresi")
    first_name = forms.CharField(max_length=25, min_length=3, label="Ad")
    last_name = forms.CharField(max_length=25, min_length=3, label="Soyad")
    password = forms.CharField(min_length=6, max_length=50, label="Şifre", widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=6, max_length=50, label="Şifre Tekrar", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Girilen şifreler uyuşmuyor! Lütfen tekrar deneyin.")

        values = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
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