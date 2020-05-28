from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import formset_factory, modelformset_factory

from article.models import ArticleComment
from course.models import CourseLecture, CourseSection, Course


class AddArticleComment(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['content', ]


class CourseForm(forms.Form):
    courseDescription = forms.CharField(widget=CKEditorWidget(), label="Yazı")
    courseIntroduction = forms.CharField(widget=CKEditorWidget(), label="Ön Bilgi")


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['description', 'introduction']


class SectionForm(forms.Form):
    sectionDescription = forms.CharField(widget=CKEditorWidget(), label="Yazı")


class LectureForm(forms.Form):
    lectureDescription = forms.CharField(widget=CKEditorWidget(), label="Yazı")


class VideoForm(forms.Form):
    videos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class CourseSectionModelForm(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ('title', )
        labels = {
            'title': 'Bölüm Başlığı'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bölüm Başlığı'
                }
            )
        }


CourseLectureFormSet = modelformset_factory(
    CourseLecture,
    fields=('title',),
    extra=1,
    widgets={
        'title': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ders Başlığı'
            }
        )
    }
)