from django import forms
from account.models import Account, Permission, Group, GroupPermission, AccountGroup, AccountPermission
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


class AdminArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ["parentId", "title", "slug", "description"]


class AdminSchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['title', 'slug', 'description', 'media', 'isActive']


class AdminDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['schoolId', 'title', 'slug', 'isActive']


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
