from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

# Admin
from account.models import Account
from article.models import ArticleCategory, ArticleSubCategory
from course.models import CourseCategory, CourseSubCategory, CourseSubToSubCategory

MAIN_CATEGORY_CHOICES = CourseCategory.id


class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())


class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ["course_category_title", "course_category_slug", "course_category_description"]


class CourseSubCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseSubCategory
        fields = ["course_category_id", "course_sub_category_title", "course_sub_category_slug",
                  "course_sub_category_description"]


class CourseSubToSubCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseSubToSubCategory
        fields = ["course_sub_category_id", "course_sub_to_sub_category_title", "course_sub_to_sub_category_slug",
                  "course_sub_to_sub_category_description"]


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ["article_category_title", "article_category_slug", "article_category_description"]


class ArticleSubCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleSubCategory
        fields = ["article_category_id", "article_sub_category_title", "article_sub_category_slug",
                  "article_sub_category_description"]


class AdminEditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_superuser", "image"]
        help_texts = {
            'is_active': None,
            'username': None,
            'email': None,
            'image': None
        }