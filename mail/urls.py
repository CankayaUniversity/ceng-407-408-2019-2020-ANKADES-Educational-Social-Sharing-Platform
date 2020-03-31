from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from mail import views

urlpatterns = [
    path('mail-gonder', views.send_mail, name="send_mail")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
