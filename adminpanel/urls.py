from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from adminpanel import views

urlpatterns = [
    # Main Urls
    path('', views.admin_index, name="admin_index"),
    path('giris-yap', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),

    # Courses
    path('kurslar/', views.courses, name="course_table"),
    path('kurslar/kurs-ekle/', views.add_course, name="add_course"),
    path('kurslar/kurs-duzenle/<slug:course_slug>', views.admin_edit_course, name="admin_edit_course"),
    path('kurslar/kurs-sil/<slug:course_slug>', views.admin_delete_course, name="admin_delete_course"),

    # Course Categories
    path('kurslar/kurs-kategorileri/', views.course_category, name="course_category"),
    path('kurslar/kategori-ekle/', views.add_course_category, name="add_course_category"),
    path('kurslar/kategori-düzenle/<slug:course_category_slug>', views.admin_edit_course_category,
         name="admin_edit_course_category"),
    path('kurslar/kurs-kategori-sil/<slug:course_category_slug>', views.admin_delete_course_category,
         name="admin_delete_course_category"),

    # Course Sub Categories
    path('kurslar/kurs-alt-kategorileri/', views.course_sub_category, name="course_sub_category"),
    path('kurslar/alt-kategori-ekle/', views.add_course_sub_category, name="add_course_sub_category"),
    path('kurslar/alt-kategori-düzenle/<slug:course_sub_category_slug>', views.admin_edit_course_sub_category,
         name="admin_edit_course_sub_category"),
    path('kurslar/kurs-alt-kategori-sil/<slug:course_sub_category_slug>', views.admin_delete_course_sub_category,
         name="admin_delete_course_sub_category"),

    # Course Sub to Sub Categories
    path('kurslar/kurs-en-alt-kategorileri/', views.course_sub_to_sub_category, name="course_sub_to_sub_category"),
    path('kurslar/en-alt-kategori-ekle/', views.add_course_sub_to_sub_category, name="add_course_sub_to_sub_category"),
    path('kurslar/en-alt-kategori-düzenle/<slug:course_sub_to_sub_category_slug>',
         views.admin_edit_course_sub_to_sub_category, name="admin_edit_course_sub_to_sub_category"),
    path('kurslar/kurs-en-alt-kategori-sil/<slug:course_sub_to_sub_category_slug>',
         views.admin_delete_course_sub_to_sub_category, name="admin_delete_course_sub_to_sub_category"),

    # User Urls
    path('kullanicilar/', views.all_users, name="all_users"),
    url(r'^profil-duzenle/(?P<username>\w+)/$', views.admin_edit_profile, name="admin_edit_profile"),

    # Group
    path('grup-ekle/', views.add_account_main_group, name="add_account_main_group"),
    path('izin-ekle/', views.add_account_main_permission, name="add_account_main_permission"),
    path('gruba-izin-ekle/', views.add_account_group_permission, name="add_account_group_permission"),
    path('kullaniciya-grup-ekle/', views.add_account_group, name="add_account_group"),
    path('kullaniciya-izin-ekle/', views.add_account_has_permission, name="add_account_has_permission"),

    path('gruplar/', views.all_groups, name="all_groups"),
    path('gruplar/grup-sil/<slug:name_slug>', views.delete_main_group,
         name="delete_main_group"),
    path('gruplar/grup-duzenle/<slug:name_slug>', views.edit_main_group,
         name="edit_main_group"),

    path('izinler/', views.all_permissions, name="all_permissions"),
    path('izinler/izin-sil/<slug:name_slug>', views.delete_main_permission,
         name="delete_main_permission"),
    path('izinler/izin-duzenle/<slug:name_slug>', views.edit_main_permission,
         name="edit_main_permission"),

]
