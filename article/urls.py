from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from article.views import views
from article.views.views import ArticleLikeToggle

urlpatterns = [
    url(r'^(?P<username>[\w-]+)/(?P<slug>[\w-]+)/$', views.article_detail, name="article_detail"),
    path('makaleler/', views.all_articles, name="all_articles"),
    path('makaleler/kategoriler/<slug:slug>', views.article_category_page, name="article_category_page"),
    path('makale-ekle/', views.add_article, name="add_article"),
    url(r'^makale/(?P<slug>[\w-]+)/sil/$', views.delete_article, name="delete_article"),
    url(r'^makale/(?P<postNumber>[\w-]+)/duzenle/$', views.edit_article, name="edit_article"),
    url(r'^makale/(?P<postNumber>[\w-]+)/sikayet-et/$', views.add_report_article, name="add_report_article"),
    path('makale/yorum-ekle/<slug:slug>/', views.add_article_comment, name="add_article_comment"),
    url(r'^makale/(?P<commentNumber>[\w-]+)/cevapla/$', views.add_article_comment_reply,
        name="add_article_comment_reply"),
    url(r'^yorum/(?P<commentNumber>[\w-]+)/duzenle/$', views.edit_article_comment,
        name="edit_article_comment"),
    url(r'^yorum/(?P<commentNumber>[\w-]+)/sil/$', views.delete_article_comment,
        name="delete_article_comment"),
    url(r'^(?P<username>[\w-]+)/(?P<slug>[\w-]+)/like/$', ArticleLikeToggle.as_view(), name="article-like-toggle"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)