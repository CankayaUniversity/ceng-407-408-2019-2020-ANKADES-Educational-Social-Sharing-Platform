from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

# Admin
from course.models import CourseCategory, CourseSubCategory, CourseSubToSubCategory, Course


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
