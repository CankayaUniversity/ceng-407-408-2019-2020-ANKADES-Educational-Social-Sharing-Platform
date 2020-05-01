from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from exam.views import schools, views

urlpatterns = [
    # url(r'^(?P<slug>[\w-]+)/bolumler/$', views.all_departments, name="all_departments"),
    # path('okullar/', schools.all_schools, name="all_schools"),

    # path('<slug:slug>/bolumler', views.all_departments, name="all_departments"),
    # path('bolum-ekle/', views.add_department, name="add_department"),
    # url(r'^bolum-ekle/(?P<slug>[\w-]+)/$', views.add_department, name="add_department"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
