from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from adminpanel import views

urlpatterns = [
    # Main Urls
    path('', views.admin_index, name="admin_index"),
    path('giris-yap', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),
]

