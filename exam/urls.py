from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from exam.views import school, lecture, department, exam

urlpatterns = [
    path('okullar/', school.all_schools, name="all_schools"),
    url(r'^okullar/(?P<slug>[\w-]+)/bolumler', department.all_departments, name="all_departments"),
    url(r'^bolum/(?P<departmentCode>[\w-]+)/dersler/$', lecture.lectures, name="lectures"),
    url(r'^ders/(?P<postNumber>[\w-]+)/sinavlar/$', exam.lecture_exam, name="lecture_exam"),
    url(r'^sinav/(?P<examNumber>[\w-]+)/sil/$', exam.delete_exam, name="delete_exam"),
    url(r'^sinav/(?P<examNumber>[\w-]+)/duzenle/$', exam.edit_exam, name="edit_exam"),
    path('bolum-ekle/', department.add_department, name="add_department"),
    path('ders-ekle/', lecture.add_lecture, name="add_lecture"),
    path('sinav-ekle/', exam.add_exam, name="add_exam"),
    # url(r'^bolum-ekle/(?P<slug>[\w-]+)/$', views.add_department, name="add_department"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
