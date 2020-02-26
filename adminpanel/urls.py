from django.conf.urls import url
from django.urls import path

from adminpanel.views import views, permission, course, account
from adminpanel.views import group

urlpatterns = [
    # Main Urls
    path('', views.admin_index, name="admin_index"),
    path('giris-yap', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),

    # kurslar/...
    path('kurslar/', course.admin_courses, name="admin_courses"),
    path('kurslar/kurs-ekle/', course.admin_add_course, name="admin_add_course"),
    path('kurslar/kurs-duzenle/<slug:slug>', course.admin_edit_course, name="admin_edit_course"),
    path('kurslar/kurs-sil/<slug:slug>', course.admin_delete_course, name="admin_delete_course"),

    # kullanicilar/...
    path('kullanicilar/', account.admin_all_users, name="admin_all_users"),
    path('kullanicilar/yasakli', account.admin_blocked_users, name="admin_blocked_users"),

    # kullanicilar/kullanici-izinleri/...
    path('kullanicilar/kullanici-izinleri/', account.admin_account_permission, name="admin_account_permission"),
    path('kullanicilar/kullanici-izinleri/ekle', account.admin_add_account_permission,
         name="admin_add_account_permission"),
    path('kullanicilar/kullanici-izinleri/duzenle/<uuid:id>', account.admin_edit_account_permission,
         name="admin_edit_account_permission"),
    path('kullanicilar/kullanici-izinleri/etkisizlestir/<uuid:id>', account.admin_deactivate_account_permission,
         name="admin_deactivate_account_permission"),
    # path('kullanicilar/kullanici-izinleri/etkinlestir/<uuid:id>', account.admin_activate_account_permission, name="admin_activate_account_permission"),
    path('kullanicilar/kullanici-izinleri/sil/<uuid:id>', account.admin_delete_account_permission,
         name="admin_delete_account_permission"),
    url(r'^profil-duzenle/(?P<username>\w+)/$', account.admin_edit_profile, name="admin_edit_profile"),
    url(r'^profil-sil/(?P<username>\w+)/$', account.admin_deactivate_profile, name="admin_deactivate_profile"),

    # kullanicilar/grup/..
    path('kullanicilar/grup/', group.admin_account_groups, name="admin_account_groups"),
    path('kullanicilar/grup/ekle/', account.admin_add_account_group, name="admin_add_account_group"),
    path('kullanicilar/grup/duzenle/<uuid:id>', account.admin_edit_account_group, name="admin_edit_account_group"),
    path('kullanicilar/grup/etkisizlestir/<uuid:id>', group.admin_deactivate_account_group,
         name="admin_deactivate_account_group"),
    path('kullanicilar/grup/sil/<uuid:id>', group.admin_delete_account_group, name="admin_delete_account_group"),

    # guplar/...
    path('gruplar/', group.admin_all_groups, name="admin_all_groups"),
    path('gruplar/ekle', group.admin_add_group, name="admin_add_group"),
    path('gruplar/duzenle/<slug:slug>', group.admin_edit_group,
         name="admin_edit_group"),
    path('gruplar/sil/<slug:slug>', group.admin_delete_group,
         name="admin_delete_group"),

    # gruplar/grup-izinleri
    path('gruplar/grup-izinleri/', group.admin_group_permission, name="admin_group_permission"),
    path('gruplar/grup-izinleri/ekle', group.admin_add_group_permission, name="admin_add_group_permission"),
    path('gruplar/grup-izinleri/sil/<uuid:id>', group.admin_delete_group_permission,
         name="admin_delete_group_permission"),
    path('gruplar/grup-izinleri/duzenle/<uuid:id>', group.admin_edit_group_permission,
         name="admin_edit_group_permission"),
    path('gruplar/grup-izinleri/duzenle/<uuid:id>', group.admin_deactivate_group_permission,
         name="admin_deactivate_group_permission"),

    # izinler/
    path('izinler/', permission.admin_all_permissions, name="admin_all_permissions"),
    path('izinler/ekle/', permission.admin_add_permission, name="admin_add_permission"),
    path('izinler/duzenle/<slug:slug>', permission.admin_edit_permission,
         name="admin_edit_permission"),
    path('izinler/sil/<slug:slug>', permission.admin_delete_permission,
         name="admin_delete_permission"),

    # izinler/role-izinleri
    path('izinler/ogrenci-izinleri', permission.admin_site_student_permission, name="admin_site_student_permission"),
    path('izinler/ogretmen-izinleri', permission.admin_site_teacher_permission, name="admin_site_teacher_permission"),
    path('izinler/moderator-izinleri', permission.admin_site_moderator_permission,
         name="admin_site_moderator_permission"),
    path('izinler/admin-izinleri', permission.admin_site_admin_permission, name="admin_site_admin_permission"),

    # kurslar/...
    path('kurslar/', course.admin_courses, name="admin_courses"),
    # path('kurslar/ekle', course.admin_add_course, name="admin_add_course"),
    path('kurslar/duzenle/<slug:slug>', course.admin_edit_course, name="admin_edit_course"),
    path('kurslar/sil/<slug:slug>', course.admin_delete_course, name="admin_delete_course"),

    # kurslar/kurs-kategorileri/...
    path('kurslar/kurs-kategorileri/', course.admin_course_category, name="admin_course_category"),
    path('kurslar/kurs-kategorileri/ekle/', course.admin_add_course_category, name="admin_add_course_category"),
    path('kurslar/kurs-kategorileri/düzenle/<slug:slug>', course.admin_edit_course_category,
         name="admin_edit_course_category"),
    path('kurslar/kurs-kategorileri/sil/<slug:slug>', course.admin_delete_course_category,
         name="admin_delete_course_category"),

]
