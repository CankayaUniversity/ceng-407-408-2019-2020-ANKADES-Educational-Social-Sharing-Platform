from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.db.models import Q
from account.models import Account, Permission, Group, SocialMedia
from adminpanel.models import Tag
from article.models import Article, ArticleCategory
from course.models import Course, CourseCategory
from exam.models import School


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


class AdminEditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'isActive']


class AdminCourseForm(forms.Form):
    categoryId = forms.ModelChoiceField(queryset=CourseCategory.objects.filter(Q(isRoot=False) and Q()),
                                        label="Kategori Adı")
    title = forms.CharField(label="Başlık")
    description = RichTextField()
    media = forms.FileField(required=False, allow_empty_file=True)
    isActive = forms.BooleanField(required=False, label="Aktif")
    isPrivate = forms.BooleanField(required=False, label="Özel")


class AdminCourseCategoryForm(forms.Form):
    parentId = forms.ModelChoiceField(queryset=CourseCategory.objects.all(), label="Kategorisi")
    title = forms.CharField(label="Başlık")
    description = RichTextField()


class AdminPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['title', 'isActive']


class AdminGroupPermissionForm(forms.Form):
    groupId = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grup Adı")
    permissionId = forms.ModelChoiceField(queryset=Permission.objects.all(), label="İzin Adı")
    isActive = forms.BooleanField(required=False, label="Aktif")


class AdminArticleForm(forms.Form):
    categoryId = forms.ModelChoiceField(queryset=ArticleCategory.objects.filter(Q(isRoot=False), Q(isActive=True), Q(isCategory=False)),
                                        label="Kategori Adı")
    title = forms.CharField(label="Başlık")
    description = forms.CharField(widget=CKEditorWidget())
    isActive = forms.BooleanField(required=False, label="Aktif olacak ise kutucuğu işaretleyin")
    isPrivate = forms.BooleanField(required=False, label="Özel olacak ise kutucuğu işaretleyin")
    media = forms.FileField(allow_empty_file=True, required=False, label="Dosya")
    tagId = forms.ModelMultipleChoiceField(queryset=Tag.objects.filter(isActive=True), label="Etiket", required=False)


class AddArticleForm(forms.Form):
    description = forms.CharField(widget=CKEditorWidget())


class AdminEditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['categoryId', 'media', 'title', 'description', 'isPrivate', 'isActive']


class AdminTagForm(forms.Form):
    title = forms.CharField(label="Başlık")
    isActive = forms.BooleanField(required=False, label="Aktiflik")


class AdminArticleCategoryForm(forms.Form):
    parentId = forms.ModelChoiceField(
        queryset=ArticleCategory.objects.all(),
        label="Üst Kategorisi")
    title = forms.CharField(max_length=254, label="Başlık")
    isActive = forms.BooleanField(label="Aktif")
    isCategory = forms.BooleanField(label="Üst Kategori", required=False)


class AdminEditArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ['parentId', 'title', 'description', 'isCategory', 'isRoot', 'isActive']


class AdminSchoolForm(forms.Form):
    title = forms.CharField(label="Okul Adı")
    description = RichTextField()
    media = forms.FileField(allow_empty_file=True, required=False, label="Dosya")
    isActive = forms.BooleanField(required=False, label="Aktif")


class AdminExamForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.filter(isActive=True), label="Okul")


class AdminExamCommentForm(forms.ModelForm):
    content = RichTextField()
    media = forms.FileField(allow_empty_file=True)


class AdminSocialMediaForm(forms.Form):
    title = forms.CharField(label="Sosyal Medya Adı")
    isActive = forms.BooleanField(label="Aktif", required=False)

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
