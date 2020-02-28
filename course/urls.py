from django.urls import path
from course import views

urlpatterns = [
    path('kurslar/', views.all_courses, name="all_courses"),
    path('kurs/<slug:slug>', views.course_detail, name="course_detail"),
]
