from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from account.views import views, edit

urlpatterns = [
    # Current User
    path('ayarlar/', edit.edit_profile, name="edit_profile"),
    path('ayarlar/resim-ekle', edit.edit_profile_photo, name="edit_profile_photo"),
    path('ayarlar/okul-ekle/', edit.edit_graduate, name="edit_graduate"),
    path('ayarlar/biyografi-ekle/', edit.edit_bio, name="edit_bio"),
    path('ayarlar/email-duzenle', edit.edit_email, name="edit_email"),
    path('ayarlar/kullanici-adi-duzenle', edit.edit_username, name="edit_username"),
    path('ayarlar/sifre-yenile', edit.edit_password, name="edit_password"),
    path('ayarlar/sosyal-medya-ekle/', edit.add_social_media_to_user, name="add_social_media_to_user"),
    url(r'^(?P<username>[\w-]+)/takip-et/$', views.follow_account, name="follow_account"),
    # path('sifre-sifirla/', edit.edit_password, name="edit_password"),

    # Login/Register
    path('giris-yap/', views.login_account, name="login_account"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
    path('kayit-ol/', views.register_account, name="register_account"),

    # Requested User
    path('', views.index, name="index"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
