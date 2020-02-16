from django.urls import path

from question import views

urlpatterns = [
    path('', views.index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)