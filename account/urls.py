from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from django.contrib.auth import views as auth_views
from account.views import views, edit, posts

urlpatterns = [
    # Current User
    path('ayarlar/', edit.edit_profile, name="edit_profile"),
    path('ayarlar/resim-ekle/', edit.edit_profile_photo, name="edit_profile_photo"),
    path('ayarlar/okul-ekle/', edit.edit_graduate, name="edit_graduate"),
    path('ayarlar/biyografi-ekle/', edit.edit_bio, name="edit_bio"),
    path('ayarlar/email-duzenle/', edit.edit_email, name="edit_email"),
    path('ayarlar/kullanici-adi-duzenle/', edit.edit_username, name="edit_username"),
    path('ayarlar/sifre-yenile/', edit.edit_password, name="edit_password"),
    path('ayarlar/konum-duzenle/', edit.edit_zone, name="edit_zone"),
    path('ayarlar/cv-duzenle/', edit.edit_cv, name="edit_cv"),
    path('ayarlar/yetenekler/', edit.edit_cv, name="edit_cv"),
    path('ayarlar/sosyal-medya-ekle/', edit.add_social_media_to_user, name="add_social_media_to_user"),
    url(r'^(?P<username>[\w-]+)/takip-et/$', views.follow_account, name="follow_account"),
    path('paylasimlarim/', posts.my_posts, name="my_posts"),
    # path('sifre-sifirla/', edit.edit_password, name="edit_password"),

    # Login/Register
    path('giris-yap/', views.login_account, name="login_account"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
    path('kayit-ol/', views.register_account, name="register_account"),

    # Requested User
    path('', views.index, name="index"),

    #Password Reset
    path('sifre-sifirla/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('sifre-sifirlama-gonderildi/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('sifre-sifirla/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('sifre-sifirlama/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
