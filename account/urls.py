from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from account import views

urlpatterns = [
    path('giris-yap/', views.login_account, name="login_account"),
    path('', views.index, name="index"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
    path('kayit-ol/', views.register_account, name="register_account"),
    url(r'^kullanicilar/(?P<username>\w+)/$', views.account_detail, name="account_detail"),
    url(r'^profil-duzenle/(?P<username>\w+)/$', views.edit_profile, name="edit_profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)