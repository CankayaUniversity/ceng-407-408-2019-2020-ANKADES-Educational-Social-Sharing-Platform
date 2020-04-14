from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from course.views import views

urlpatterns = [
    path('kurslar/', views.all_courses, name="all_courses"),
    # path('kurs-ekle/', views.all_courses, name="all_courses"),
    path('kurslar/kategoriler/<slug:slug>', views.course_category_page, name="course_category_page"),
    path('kurs-ekle/', views.add_course, name="add_course"),
    path('kurs/<slug:slug>', views.course_detail, name="course_detail"),
    # path('kurs/<slug:slug>', views.course_detail, name="course_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)