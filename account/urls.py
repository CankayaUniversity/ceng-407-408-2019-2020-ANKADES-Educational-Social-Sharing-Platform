from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from account.views import views, user, edit, posts
# from account.views.api import UserProfileView, UserRegistrationView, UserLoginView, AccountGroupView, \
#     FollowAccountAPIToggle
from account.views.views import FollowAccountToggle
from article.views import views as articleviews

urlpatterns = [
    # Current User
    path('ayarlar/', edit.edit_profile, name="edit_profile"),
    path('ayarlar/email-duzenle', edit.edit_email, name="edit_email"),
    path('paylasimlarim/', posts.user_posts, name="user_posts"),
    path('ayarlar/kullanici-adi-duzenle', edit.edit_username, name="edit_username"),
    path('ayarlar/sifre-yenile', edit.edit_password, name="edit_password"),
    path('ayarlar/sosyal-medya-ekle', edit.add_social_media_to_user, name="add_social_media_to_user"),
    # path('sifre-sifirla/', edit.edit_password, name="edit_password"),

    # Login/Register
    path('giris-yap/', views.login_account, name="login_account"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
    path('kayit-ol/', views.register_account, name="register_account"),

    # Requested User
    # url(r'^Article/(?P<username>[\w-]+)/Follow/$', FollowAccountAPIToggle.as_view(), name="follow-api-toggle"),
    path('', views.index, name="index"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
