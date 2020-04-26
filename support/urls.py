from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from support import views

urlpatterns = [
    # url(r'^report/(?P<postNumber>[\w-]+)/$', views.add_report_article, name="add_report_article"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
