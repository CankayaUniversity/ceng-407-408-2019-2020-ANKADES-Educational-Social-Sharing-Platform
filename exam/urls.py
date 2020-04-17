from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from exam.views import schools

urlpatterns = [
    path('okullar/', schools.all_schools, name="all_schools"),
    # path('bolumler/', departments.all_departments, name="all_departments"),
    # path('dersler/', views.all_lectures, name="all_lectures"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)