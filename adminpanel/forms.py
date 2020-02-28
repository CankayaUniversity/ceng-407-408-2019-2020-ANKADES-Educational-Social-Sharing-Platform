from django import forms
from account.models import Account, Permission, Group, GroupPermission, AccountGroup, AccountPermission
from article.models import Article, ArticleCategory
from course.models import Course, CourseCategory
from exam.models import School, Department, Lecture, Term, Exam, ExamComment


class AdminLoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())


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


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "slug", "categoryId", "isActive", "isPrivate", "media", "description"]


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ["parentId", "title", "slug", "description"]


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["title", "slug", "description", "isActive", "since", "media"]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["schoolId", "title", "slug", "description", "isActive"]


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ["departmentId", "term", "slug"]


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ["departmentId", "termId", "title", "slug", "description", "isActive", "media"]


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["lectureId", "title", "slug", "description", "isActive", "media"]


class ExamCommentForm(forms.ModelForm):
    class Meta:
        model = ExamComment
        fields = ["content", "media"]


