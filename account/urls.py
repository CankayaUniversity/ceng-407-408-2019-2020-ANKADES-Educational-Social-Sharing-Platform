from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from account.views import views, restview
from account.views.restview import UserProfileView, UserRegistrationView, UserLoginView, AccountGroupView

urlpatterns = [
    path('giris-yap/', views.login_account, name="login_account"),
    path('', views.index, name="index"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
    path('kayit-ol/', views.register_account, name="register_account"),
    url(r'^kullanicilar/(?P<username>\w+)/$', views.account_detail, name="account_detail"),
    url(r'^profil-duzenle/(?P<username>\w+)/$', views.edit_profile, name="edit_profile"),
    url(r'^sifre-sifirla/(?P<username>\w+)/$', views.edit_password, name="edit_password"),
    url(r'^kullaniciadi-duzenle/(?P<username>\w+)/$', views.edit_username, name="edit_username"),

    #rest view
    url(r'^Account/Profile/', UserProfileView.as_view()),
    url(r'^Account/Register/', UserRegistrationView.as_view()),
    url(r'^Account/Login/', UserLoginView.as_view()),
    url(r'^Account/Group/', AccountGroupView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
