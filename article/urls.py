from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from article import views

urlpatterns = [
    path('makaleler/', views.all_articles, name="all_articles"),
    path('makale/ekle', views.add_article, name="add_article"),
    path('makale/<slug:slug>', views.article_detail, name="article_detail"),
    path('makale/sil/<slug:slug>', views.article_delete, name="article_delete"),
    path('makale/duzenle/<slug:slug>', views.article_edit, name="article_edit"),
    url(r'^makale/makalelerim/(?P<username>\w+)/$', views.my_articles, name="my_articles"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)