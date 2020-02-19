from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

# Admin
from account.models import Account, MainPermission, MainGroup, AccountGroupPermission, AccountGroup, \
    AccountHasPermission
from article.models import ArticleCategory, ArticleSubCategory
from course.models import CourseCategory, CourseSubCategory, CourseSubToSubCategory, Course

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


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_sub_to_sub_category_id", "course_title", "course_slug", "course_content",
                  "course_media"]


class AddAccountMainPermissionForm(forms.ModelForm):
    class Meta:
        model = MainPermission
        fields = ["name", "name_slug"]


class AddAccountMainGroupForm(forms.ModelForm):
    class Meta:
        model = MainGroup
        fields = ["name", "name_slug"]


class AddAccountGroupPermissionForm(forms.ModelForm):
    class Meta:
        model = AccountGroupPermission
        fields = ["permission_id", "group_id"]


class AddAccountGroupForm(forms.ModelForm):
    class Meta:
        model = AccountGroup
        fields = ["user_id", "group_id"]


class AddAccountHasPermission(forms.ModelForm):
    class Meta:
        model = AccountHasPermission
        fields = ["user_id", "permission_id"]