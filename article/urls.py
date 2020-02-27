from django.conf.urls import url
from django.urls import path

from article import views

urlpatterns = [
    path('makaleler/', views.all_articles, name="all_articles"),
    path('makale/<slug:slug>', views.article_detail, name="article_detail"),
]