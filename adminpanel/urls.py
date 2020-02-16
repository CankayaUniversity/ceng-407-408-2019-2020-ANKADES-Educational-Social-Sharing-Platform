from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from adminpanel import views

urlpatterns = [
    # Main Urls
    path('', views.admin_index, name="admin_index"),
    path('giris-yap', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),
    path('kullanicilar/', views.users_table, name="users_table"),
    path('kurslar/', views.course_table, name="course_table"),
    path('kurs-kategori-ekle/', views.add_course_category, name="add_course_category"),
    path('kurs-alt-kategori-ekle/', views.add_course_sub_category, name="add_course_sub_category"),
    path('kurs-en-alt-kategori-ekle/', views.add_course_sub_to_subcategory, name="add_course_sub_to_subcategory"),
]

