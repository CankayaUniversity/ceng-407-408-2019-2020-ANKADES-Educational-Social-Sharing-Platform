from django.urls import path

from exam.views import schools, departments

urlpatterns = [
    path('okullar/', schools.all_schools, name="all_schools"),
    path('bolumler/', departments.all_departments, name="all_departments"),
    # path('dersler/', views.all_lectures, name="all_lectures"),
]