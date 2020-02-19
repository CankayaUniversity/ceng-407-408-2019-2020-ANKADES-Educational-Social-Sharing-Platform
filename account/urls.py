from django.urls import path

# from question import views
from account import views

urlpatterns = [
    # path('', views.index, name="index"),
    path('giris-yap/', views.login_account, name="login_account"),
    path('', views.index, name="index"),
    path('cikis-yap/', views.logout_account, name="logout_account"),
]