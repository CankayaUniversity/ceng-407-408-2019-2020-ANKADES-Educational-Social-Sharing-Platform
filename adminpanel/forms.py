from ckeditor.fields import RichTextField
from django import forms
from django.db.models import Q

from account.models import Account, Permission, Group, GroupPermission, AccountGroup, AccountPermission
from adminpanel.models import Tag
from article.models import Article, ArticleCategory
from course.models import Course, CourseCategory
from exam.models import School, Department, Lecture, Exam, ExamComment, Term


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


class AdminCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "categoryId", "isActive", "isPrivate", "media", "description"]


class AdminCourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ["parentId", "title", "slug", "description"]


class AdminPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ["title", "slug", "isActive"]


class AdminGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["title", "slug", "isActive"]


class AdminGroupPermissionForm(forms.ModelForm):
    class Meta:
        model = GroupPermission
        fields = ["groupId", "permissionId", "isActive"]


class AdminAccountGroupForm(forms.ModelForm):
    class Meta:
        model = AccountGroup
        fields = ["userId", "groupId", "isActive"]


class AdminAccountPermissionForm(forms.ModelForm):
    class Meta:
        model = AccountPermission
        fields = ["userId", "permissionId", "isActive"]


class AdminArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "slug", "categoryId", "isActive", "isPrivate", "media", "description"]


class AdminTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug', 'isActive']


# class AdminArticleForm(forms.Form):
#     title = forms.CharField(max_length=None, label="Başlık")
#     slug = forms.SlugField(max_length=None, label="Slug")
#     tag = forms.ModelChoiceField(queryset=Tag.objects.filter(isActive=True), label="Etiket Seçin")
#     description = RichTextField()


class AdminArticleCategoryForm(forms.Form):
    parentId = forms.BooleanField(required=False, initial=True)
    if parentId is True:
        categoryId = forms.ModelChoiceField(queryset=ArticleCategory.objects.filter(Q(isCategory=True)))
    else:
        categoryId = forms.ModelChoiceField(
            queryset=ArticleCategory.objects.filter(Q(isRoot=False) and Q(isCategory=False)),
            label="Üst Kategorisi")
    title = forms.CharField(max_length=254, label="Başlık")
    slug = forms.SlugField(max_length=254, label="Slug")
    isActive = forms.BooleanField(label="Aktiflik")
    isCategory = forms.BooleanField(label="Üst Kategori mi")


class AdminSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['title', 'slug', 'description', 'media', 'isActive']


class AdminDepartmentForm(forms.Form):
    schoolId = forms.ModelChoiceField(queryset=School.objects.filter(Q(isActive=True)), label="Okul")
    title = forms.CharField(max_length=254, label="Başlık")
    slug = forms.SlugField(max_length=254, label="Slug")
    isActive = forms.BooleanField(label="Aktiflik")


class AdminTermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['departmentId', 'title', 'slug', 'isActive']


class AdminLectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['termId', 'title', 'slug', 'description', 'isActive']


class AdminExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['lectureId', 'title', 'slug', 'description', 'isActive', 'media']


class AdminExamCommentForm(forms.ModelForm):
    class Meta:
        model = ExamComment
        fields = '__all__'


class AdminSocialMediaForm(forms.Form):
    title = forms.CharField(label="Sosyal Medya Adı")
    slug = forms.SlugField(max_length=None, label="Slug")
    isActive = forms.BooleanField(label="Aktiflik", required=False)