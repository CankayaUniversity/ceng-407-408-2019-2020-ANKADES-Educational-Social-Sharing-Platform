from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from article import views
from article.views import ArticleLikeToggle, ArticleLikeAPIToggle

urlpatterns = [
    path('makaleler/', views.all_articles, name="all_articles"),
    path('makale/ekle/', views.add_article, name="add_article"),
    path('makale/<slug:slug>/', views.article_detail, name="article_detail"),
    path('makale/sil/<slug:slug>/', views.delete_article, name="delete_article"),
    path('makale/duzenle/<slug:slug>/', views.edit_article, name="edit_article"),
    url(r'^makale/makalelerim/(?P<username>\w+)/$', views.my_articles, name="my_articles"),
    path('makale/yorum-ekle/<slug:slug>/', views.add_article_comment, name="add_article_comment"),
    url(r'^(?P<slug>[\w-]+)/begen/$', ArticleLikeToggle.as_view(), name="like-toggle"),
    url(r'^Article/(?P<slug>[\w-]+)/Begen/$', ArticleLikeAPIToggle.as_view(), name="like-api-toggle"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)