from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from adminpanel.views import group
from adminpanel.views import views, permission, course, account, article, exam

urlpatterns = [
    # Main Url
    path('', views.admin_index, name="admin_index"),
    path('ayarlar/site', views.admin_settings, name="admin_settings"),
    path('ayarlar/hesap', views.admin_account_settings, name="admin_account_settings"),
    path('ayarlar/sosyal-medya', views.admin_social_media_settings, name="admin_social_media_settings"),
    path('ayarlar/sosyal-medya/ekle', views.admin_add_social_media, name="admin_add_social_media"),
    path('ayarlar/grup', views.admin_group_settings, name="admin_group_settings"),
    path('ayarlar/izin', views.admin_permission_settings, name="admin_permission_settings"),
    path('ayarlar/yeni-kullanici-ekle', account.admin_register_account, name="admin_register_account"),
    path('giris-yap/', views.login_admin, name="login_admin"),
    path('cikis/', views.logout_admin, name="logout_admin"),

    # User
    path('kullanicilar/', account.admin_all_users, name="admin_all_users"),
    path('kullanicilar/ogrenciler/', account.admin_students, name="admin_students"),
    path('kullanicilar/ogretmenler/', account.admin_teachers, name="admin_teachers"),
    path('kullanicilar/moderatorler', account.admin_moderators, name="admin_moderators"),
    path('kullanicilar/adminler', account.admin_admins, name="admin_admins"),
    path('kullanicilar/yasakli', account.admin_blocked_users, name="admin_blocked_users"),

    # User Permission
    path('kullanicilar/kullanici-izinleri/', account.admin_account_permission, name="admin_account_permission"),
    path('kullanicilar/kullanici-izinleri/ekle/', account.admin_add_account_permission,
         name="admin_add_account_permission"),
    path('kullanicilar/kullanici-izinleri/duzenle/<uuid:id>', account.admin_edit_account_permission,
         name="admin_edit_account_permission"),
    path('kullanicilar/kullanici-izinleri/etkisizlestir/<uuid:id>', account.admin_deactivate_account_permission,
         name="admin_deactivate_account_permission"),
    path('kullanicilar/kullanici-izinleri/sil/<uuid:id>', account.admin_delete_account_permission,
         name="admin_delete_account_permission"),
    url(r'^profil-duzenle/(?P<username>\w+)/$', account.admin_edit_profile, name="admin_edit_profile"),
    url(r'^profil-sil/(?P<username>\w+)/$', account.admin_deactivate_profile, name="admin_deactivate_profile"),

    # User Group
    path('kullanicilar/grup/', group.admin_account_groups, name="admin_account_groups"),
    path('kullanicilar/grup/ekle/', account.admin_add_account_group, name="admin_add_account_group"),
    path('kullanicilar/grup/duzenle/<uuid:id>', account.admin_edit_account_group, name="admin_edit_account_group"),
    path('kullanicilar/grup/etkinlestirme/<uuid:id>', group.admin_deactivate_account_group,
         name="admin_deactivate_account_group"),
    path('kullanicilar/grup/sil/<uuid:id>', group.admin_delete_account_group, name="admin_delete_account_group"),

    # Group
    path('gruplar/', group.admin_all_groups, name="admin_all_groups"),
    path('gruplar/ekle', group.admin_add_group, name="admin_add_group"),
    path('gruplar/duzenle/<slug:slug>', group.admin_edit_group,
         name="admin_edit_group"),
    path('gruplar/sil/<slug:slug>', group.admin_delete_group,
         name="admin_delete_group"),
    path('gruplar/etkinlestirme/<slug:slug>', group.admin_activation_edit_group,
         name="admin_activation_edit_group"),

    # Group Permission
    path('gruplar/grup-izinleri/', group.admin_group_permission, name="admin_group_permission"),
    path('gruplar/grup-izinleri/ekle', group.admin_add_group_permission, name="admin_add_group_permission"),
    path('gruplar/grup-izinleri/sil/<uuid:id>', group.admin_delete_group_permission,
         name="admin_delete_group_permission"),
    path('gruplar/grup-izinleri/duzenle/<uuid:id>', group.admin_edit_group_permission,
         name="admin_edit_group_permission"),
    path('gruplar/grup-izinleri/duzenle/<uuid:id>', group.admin_deactivate_group_permission,
         name="admin_deactivate_group_permission"),

    # Permission
    path('izinler/', permission.admin_all_permissions, name="admin_all_permissions"),
    path('izinler/ekle/', permission.admin_add_permission, name="admin_add_permission"),
    path('izinler/duzenle/<slug:slug>', permission.admin_edit_permission,
         name="admin_edit_permission"),
    path('izinler/sil/<slug:slug>', permission.admin_delete_permission,
         name="admin_delete_permission"),

    # User Permission
    path('izinler/ogrenci-izinleri', permission.admin_site_student_permission, name="admin_site_student_permission"),
    path('izinler/ogretmen-izinleri', permission.admin_site_teacher_permission, name="admin_site_teacher_permission"),
    path('izinler/moderator-izinleri', permission.admin_site_moderator_permission,
         name="admin_site_moderator_permission"),
    path('izinler/admin-izinleri', permission.admin_site_admin_permission, name="admin_site_admin_permission"),

    # Course
    path('kurslar/', course.admin_courses, name="admin_courses"),
    path('kurslar/ekle', course.admin_add_course, name="admin_add_course"),
    path('kurslar/duzenle/<slug:slug>', course.admin_edit_course, name="admin_edit_course"),
    path('kurslar/sil/<slug:slug>', course.admin_delete_course, name="admin_delete_course"),

    # Course Category
    path('kurslar/kurs-kategorileri/', course.admin_course_category, name="admin_course_category"),
    path('kurslar/kurs-kategorileri/ekle/', course.admin_add_course_category, name="admin_add_course_category"),
    path('kurslar/kurs-kategorileri/düzenle/<slug:slug>', course.admin_edit_course_category,
         name="admin_edit_course_category"),
    path('kurslar/kurs-kategorileri/sil/<slug:slug>', course.admin_delete_course_category,
         name="admin_delete_course_category"),

    # Article
    path('makaleler/', article.admin_articles, name="admin_articles"),
    path('makaleler/ekle', article.admin_add_article, name="admin_add_article"),
    path('makaleler/duzenle/<slug:slug>', article.admin_edit_article, name="admin_edit_article"),
    path('makaleler/sil/<slug:slug>', article.admin_delete_article, name="admin_delete_article"),
    path('makaleler/etiketler', article.admin_tags, name="admin_tags"),
    path('makaleler/etiketler/ekle', article.admin_add_tag, name="admin_add_tag"),

    # Article Category
    path('makaleler/makale-kategorileri/', article.admin_article_category, name="admin_article_category"),
    path('makaleler/makale-kategorileri/ekle/', article.admin_add_article_category, name="admin_add_article_category"),
    path('makaleler/makale-kategorileri/düzenle/<slug:slug>', article.admin_edit_article_category,
         name="admin_edit_article_category"),
    path('makaleler/makale-kategorileri/sil/<slug:slug>', article.admin_delete_article_category,
         name="admin_delete_article_category"),

    # School
    path('okullar/', exam.admin_schools, name="admin_schools"),
    path('okullar/ekle', exam.admin_add_school, name="admin_add_school"),
    path('okullar/duzenle/<slug:slug>', exam.admin_edit_school, name="admin_edit_school"),
    path('okullar/sil/<slug:slug>', exam.admin_delete_school, name="admin_delete_school"),

    # Department
    path('okullar/bolumler/', exam.admin_departments, name="admin_departments"),
    path('okullar/bolum/ekle/', exam.admin_add_department, name="admin_add_department"),
    path('okullar/bolum/düzenle/<slug:slug>', exam.admin_edit_department,
         name="admin_edit_department"),
    path('kurslar/bolum/sil/<slug:slug>', exam.admin_delete_department,
         name="admin_delete_department"),
    path('okullar/bolum/donem-ekle/', exam.admin_add_term, name="admin_add_term"),

    #Term
    path('okullar/bolumler/donemler/', exam.admin_terms, name="admin_terms"),
    path('okullar/donem/ekle/', exam.admin_add_term, name="admin_add_term"),
    path('okullar/donem/duzenle/<slug:slug>', exam.admin_edit_term,
         name="admin_edit_term"),
    path('okullar/donem/sil/<slug:slug>', exam.admin_delete_term,
         name="admin_delete_term"),

    #Lecture
    path('okullar/bolumler/donemler/ders', exam.admin_lectures, name="admin_lectures"),
    path('okullar/bolumler/donemler/ders/ekle/', exam.admin_add_lecture, name="admin_add_lecture"),
    path('okullar/bolumler/donemler/ders/duzenle/<slug:slug>', exam.admin_edit_lecture,
         name="admin_edit_lecture"),
    path('okullar/bolumler/donemler/ders/sil/<slug:slug>', exam.admin_delete_lecture,
         name="admin_delete_lecture"),

    #Exam
    path('okullar/bolumler/donemler/dersler/sinav-arsivi', exam.admin_exams, name="admin_exams"),
    path('okullar/bolumler/donemler/dersler/sinav-arsivi/ekle/', exam.admin_add_exam, name="admin_add_exam"),
    path('okullar/bolumler/donemler/dersler/sinav-arsivi/duzenle/<slug:slug>', exam.admin_edit_exam,
         name="admin_edit_exam"),
    path('okullar/bolumler/donemler/dersler/sinav-arsivi/sil/<slug:slug>', exam.admin_delete_exam,
         name="admin_delete_exam"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
