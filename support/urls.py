from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from support import views

urlpatterns = [
    url(r'^report/(?P<getNumber>[\w-]+)/$', views.add_report, name="add_report"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
