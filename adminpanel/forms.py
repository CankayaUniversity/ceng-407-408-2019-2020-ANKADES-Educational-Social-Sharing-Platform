from ckeditor.fields import RichTextField
from django import forms
from django.db.models import Q

from account.models import Account, Permission, Group, GroupPermission, AccountGroup, AccountPermission, SocialMedia
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


class AdminCourseForm(forms.Form):
    categoryId = forms.ModelChoiceField(queryset=CourseCategory.objects.filter(Q(isRoot=False) and Q()),
                                        label="Kategori Adı")
    title = forms.CharField(max_length=None, label="Başlık")
    description = RichTextField()
    media = forms.FileField(required=False, allow_empty_file=True)
    isActive = forms.BooleanField(required=False, label="Aktiflik")
    isPrivate = forms.BooleanField(required=False, label="Özellik")


class AdminCourseCategoryForm(forms.Form):
    parentId = forms.ModelChoiceField(queryset=CourseCategory.objects.all(), label="Kategorisi")
    title = forms.CharField(max_length=None, label="Başlık")
    description = RichTextField()


class AdminPermissionForm(forms.Form):
    title = forms.CharField(max_length=None, label="Başlık")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminGroupForm(forms.Form):
    title = forms.CharField(max_length=None, label="Başlık")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminGroupPermissionForm(forms.Form):
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grup Adı")
    permissionId = forms.ModelChoiceField(queryset=Permission.objects.all(), label="İzin Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminAccountGroupForm(forms.ModelForm):
    class Meta:
        model = AccountGroup
        fields = ['userId', 'groupId', 'isActive']


class AdminAccountPermissionForm(forms.Form):
    userId = forms.ModelChoiceField(queryset=Account.objects.all(), label="Kullanıcı Adı")
    permissionId = forms.ModelChoiceField(queryset=Permission.objects.all(), label="İzin Adı")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminArticleForm(forms.Form):
    categoryId = forms.ModelChoiceField(queryset=ArticleCategory.objects.filter(Q(isRoot=False) and Q()),
                                        label="Kategori Adı")
    title = forms.CharField(max_length=None, label="Başlık")
    description = RichTextField()
    isActive = forms.BooleanField(required=False, label="Aktiflik")
    isPrivate = forms.BooleanField(required=False, label="Özellik")
    media = forms.FileField(allow_empty_file=True, required=False, label="Dosya")


class AdminTagForm(forms.ModelForm):
    title = forms.CharField(max_length=None, label="Başlık")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminArticleCategoryForm(forms.Form):
    parentId = forms.ModelChoiceField(
        queryset=ArticleCategory.objects.filter(Q(isRoot=False) and Q(isCategory=True)),
        label="Üst Kategorisi")
    title = forms.CharField(max_length=254, label="Başlık")
    isActive = forms.BooleanField(label="Aktiflik")
    isCategory = forms.BooleanField(label="Üst Kategori mi")


class AdminEditArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ['parentId', 'title', 'description', 'isCategory', 'isRoot', 'isActive']


class AdminSchoolForm(forms.ModelForm):
    title = forms.CharField(max_length=None, label="Okul Adı")
    description = RichTextField()
    media = forms.FileField(allow_empty_file=True, required=False, label="Dosya")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminDepartmentForm(forms.Form):
    schoolId = forms.ModelChoiceField(queryset=School.objects.filter(Q(isActive=True)), label="Okul")
    title = forms.CharField(max_length=None, label="Başlık")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminTermForm(forms.Form):
    departmentId = forms.ModelChoiceField(queryset=Department.objects.filter(isActive=True))
    title = forms.CharField(max_length=None, label="Dönem")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminLectureForm(forms.Form):
    termId = forms.ModelChoiceField(queryset=Term.objects.filter(isActive=True))
    title = forms.CharField(max_length=None, label="Ders Adı")
    description = RichTextField()
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminExamForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.filter(isActive=True), label="Okul")


class AdminExamCommentForm(forms.ModelForm):
    content = RichTextField()
    media = forms.FileField(max_length=None, allow_empty_file=True)


class AdminSocialMediaForm(forms.Form):
    title = forms.CharField(label="Sosyal Medya Adı")
    isActive = forms.BooleanField(label="Aktiflik", required=False)

    def clean(self):
        title = self.cleaned_data.get("title")
        isActive = self.cleaned_data.get("isActive")

        values = {
            "title": title,
            "isActive": isActive,
        }
        return values


class AdminEditSocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['title', 'slug', 'isActive']
