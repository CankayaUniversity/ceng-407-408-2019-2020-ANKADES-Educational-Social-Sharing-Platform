from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from account.views import views, user
# from account.views.api import UserProfileView, UserRegistrationView, UserLoginView, AccountGroupView, \
#     FollowAccountAPIToggle
from account.views.views import FollowAccountToggle

urlpatterns = [
    path('giris-yap/', views.login_account, name="login_account"),
    path('', user.index, name="index"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
    path('kayit-ol/', views.register_account, name="register_account"),
    # url(r'^kullanicilar/(?P<username>\w+)/$', views.account_detail, name="account_detail"),
    # url(r'^(?P<username>\w+)/profil-duzenle$', views.edit_profile, name="edit_profile"),
    url(r'^(?P<username>\w+)/$', views.my_account, name="my_account"),
    url(r'^sifre-sifirla/(?P<username>\w+)/$', views.edit_password, name="edit_password"),
    # url(r'^kullanici-adi-duzenle/(?P<username>\w+)/$', views.edit_username, name="edit_username"),
    url(r'^(?P<username>[\w-]+)/takip/$', FollowAccountToggle.as_view(), name="follow-toggle"),
    # url(r'^Article/(?P<username>[\w-]+)/Follow/$', FollowAccountAPIToggle.as_view(), name="follow-api-toggle"),

    #rest view
    # url(r'^Account/Profile/', UserProfileView.as_view()),
    # url(r'^Account/Register/', UserRegistrationView.as_view()),
    # url(r'^Account/Login/', UserLoginView.as_view()),
    # url(r'^Account/Group/', AccountGroupView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
