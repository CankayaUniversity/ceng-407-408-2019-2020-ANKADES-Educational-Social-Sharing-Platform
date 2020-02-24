from django import forms
from account.models import Account, Permission, Group, GroupPermission, AccountGroup, AccountPermission
from course.models import Course, CourseCategory


class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())

# class ArticleCategoryForm(forms.ModelForm):
#     class Meta:
#         model = ArticleCategory
#         fields = ["article_category_title", "article_category_slug", "article_category_description"]
#
#
# class ArticleSubCategoryForm(forms.ModelForm):
#     class Meta:
#         model = ArticleSubCategory
#         fields = ["article_category_id", "article_sub_category_title", "article_sub_category_slug",
#                   "article_sub_category_description"]
#
#
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
        fields = ["title", "slug", "categoryId", "isActive", "isPrivate", "media", "description"]


class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ["parentId", "title", "slug", "description"]


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ["title", "slug", "isActive"]


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["title", "slug", "isActive"]


class GroupPermissionForm(forms.ModelForm):
    class Meta:
        model = GroupPermission
        fields = ["groupId", "permissionId", "isActive"]


class AccountGroupForm(forms.ModelForm):
    class Meta:
        model = AccountGroup
        fields = ["userId", "groupId", "isActive"]


class AccountPermissionForm(forms.ModelForm):
    class Meta:
        model = AccountPermission
        fields = ["userId", "permissionId", "isActive"]