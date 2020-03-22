from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from adminpanel.views import group, socialmedia
from adminpanel.views import views, account, article
from adminpanel.views.group import IsActiveGroupToggle, IsActiveGroupAPIToggle

urlpatterns = [
    # Main Url
    path('admin/', views.admin_dashboard, name="admin_dashboard"),
    path('admin/ayarlar/site', views.admin_settings, name="admin_settings"),
    path('admin/ayarlar/hesap', views.admin_account_settings, name="admin_account_settings"),
    path('admin/ayarlar/grup', views.admin_group_settings, name="admin_group_settings"),
    path('admin/ayarlar/izin', views.admin_permission_settings, name="admin_permission_settings"),
    # path('ayarlar/yeni-kullanici-ekle', account.admin_register_account, name="admin_register_account"),
    path('admin/giris-yap/', views.login_admin, name="login_admin"),
    path('admin/cikis/', views.logout_admin, name="logout_admin"),

    # User
    path('admin/kullanicilar/', account.admin_all_users, name="admin_all_users"),
    path('admin/kullanicilar/gruplari', account.admin_all_user_groups, name="admin_all_user_groups"),
    path('admin/kullanicilar/engelliler', account.admin_blocked_users, name="admin_blocked_users"),
    url(r'^admin/profil/(?P<username>[\w-]+)/$', account.admin_my_account, name="admin_my_account"),
    url(r'^admin/kullanicilar/engelle/(?P<username>\w+)/$', account.admin_block_account, name="admin_block_account"),
    url(r'^admin/kullanicilar/ogrenciler/', account.admin_students, name="admin_students"),
    url(r'^admin/kullanicilar/ogretmenler/', account.admin_teachers, name="admin_teachers"),
    url(r'^admin/kullanicilar/moderatorler', account.admin_moderators, name="admin_moderators"),
    url(r'^admin/kullanicilar/adminler', account.admin_admins, name="admin_admins"),

    # User Permission
    # path('kullanicilar/kullanici-izinleri/', account.admin_account_permission, name="admin_account_permission"),
    # path('kullanicilar/kullanici-izinleri/ekle/', account.admin_add_account_permission,
    #      name="admin_add_account_permission"),
    # path('kullanicilar/kullanici-izinleri/duzenle/<uuid:id>', account.admin_edit_account_permission,
    #      name="admin_edit_account_permission"),
    # path('kullanicilar/kullanici-izinleri/sil/<uuid:id>', account.admin_deactivate_account_permission,
    #      name="admin_deactivate_account_permission"),
    url(r'^admin/profil-duzenle/(?P<username>\w+)/$', account.admin_edit_profile, name="admin_edit_profile"),
    # url(r'^admin/profil-duzenle/resim/(?P<username>\w+)/$', account.edit_profile_photo, name="edit_profile_photo"),
    #
    # # User Group
    # path('kullanicilar/grup/', group.admin_account_groups, name="admin_account_groups"),
    # path('kullanicilar/grup/ekle/', account.admin_add_account_group, name="admin_add_account_group"),
    # path('kullanicilar/grup/duzenle/<uuid:id>', account.admin_edit_account_group, name="admin_edit_account_group"),
    # path('kullanicilar/grup/sil/<uuid:id>', group.admin_delete_account_group, name="admin_delete_account_group"),

    # Group
    url(r'^admin/gruplar/', group.admin_all_groups, name="admin_all_groups"),
    # url(r'^admin/(?P<slug>[\w-]+)/isactive/$', IsActiveGroupToggle.as_view(), name="active-toggle"),

    url(r'^admin/gruplar/ekle/', group.admin_add_group, name="admin_add_group"),
    path('admin/gruplar/<slug:slug>/duzenle', group.admin_edit_group, name="admin_edit_group"),
    url(r'^admin/grup/sil/(?P<slug>\w+)/$', group.admin_delete_group,
        name="admin_delete_group"),
    url(r'^(?P<slug>[\w-]+)/isactive/$', IsActiveGroupToggle.as_view(), name="active-toggle"),
    url(r'^AdminPanel/Group/(?P<slug>[\w-]+)/IsActive/$', IsActiveGroupAPIToggle.as_view(), name="active-api-toggle"),
    url(r'^admin/gruplar/aktiflik/<slug:slug>', group.admin_isactive_group,
        name="admin_isactive_group"),
    #
    # # Group Permission
    # path('gruplar/grup-izinleri/', group.admin_group_permission, name="admin_group_permission"),
    # path('gruplar/grup-izinleri/ekle', group.admin_add_group_permission, name="admin_add_group_permission"),
    # path('gruplar/grup-izinleri/sil/<uuid:id>', group.admin_delete_group_permission,
    #      name="admin_delete_group_permission"),
    # path('gruplar/grup-izinleri/duzenle/<uuid:id>', group.admin_edit_group_permission,
    #      name="admin_edit_group_permission"),
    #
    # # Permission
    # path('izinler/', permission.admin_all_permissions, name="admin_all_permissions"),
    # path('izinler/ekle/', permission.admin_add_permission, name="admin_add_permission"),
    # path('izinler/duzenle/<slug:slug>', permission.admin_edit_permission,
    #      name="admin_edit_permission"),
    # path('izinler/sil/<slug:slug>', permission.admin_delete_permission,
    #      name="admin_delete_permission"),
    #
    # # User Permission
    # path('izinler/ogrenci-izinleri', permission.admin_site_student_permission, name="admin_site_student_permission"),
    # path('izinler/ogretmen-izinleri', permission.admin_site_teacher_permission, name="admin_site_teacher_permission"),
    # path('izinler/moderator-izinleri', permission.admin_site_moderator_permission,
    #      name="admin_site_moderator_permission"),
    # path('izinler/admin-izinleri', permission.admin_site_admin_permission, name="admin_site_admin_permission"),
    #
    # # Course
    # path('kurslar/', course.admin_courses, name="admin_courses"),
    # path('kurslar/ekle', course.admin_add_course, name="admin_add_course"),
    # path('kurslar/duzenle/<slug:slug>', course.admin_edit_course, name="admin_edit_course"),
    # path('kurslar/sil/<slug:slug>', course.admin_delete_course, name="admin_delete_course"),
    #
    # # Course Category
    # path('kurslar/kurs-kategorileri/', course.admin_course_category, name="admin_course_category"),
    # path('kurslar/kurs-kategorileri/ekle/', course.admin_add_course_category, name="admin_add_course_category"),
    # path('kurslar/kurs-kategorileri/düzenle/<slug:slug>', course.admin_edit_course_category,
    #      name="admin_edit_course_category"),
    # path('kurslar/kurs-kategorileri/sil/<slug:slug>', course.admin_delete_course_category,
    #      name="admin_delete_course_category"),

    # Article
    path('admin/makaleler/', article.admin_all_articles, name="admin_all_articles"),
    path('admin/makale-ekle', article.admin_add_article, name="admin_add_article"),
    path('makaleler/<slug:slug>/isactive/', article.admin_isactive_article, name="admin_isactive_article"),
    path('makaleler/<slug:slug>/sil/', article.admin_delete_article, name="admin_delete_article"),
    # path('makale/<slug:slug>/duzenle/', article.admin_edit_article, name="admin_edit_article"),

    # Tag
    path('admin/etiketler/', views.admin_tags, name="admin_tags"),
    path('admin/etiket/ekle', views.admin_add_tag, name="admin_add_tag"),
    # path('etiketler/duzenle/<slug:slug>', article.admin_edit_tag, name="admin_edit_tag"),
    # path('etiketler/sil/<slug:slug>', article.admin_delete_tag, name="admin_delete_tag"),
    #

    # Article Category
    path('admin/makale-kategorileri/', article.admin_article_categories, name="admin_article_categories"),
    path('admin/makale-kategorileri/isactive/<slug:slug>', article.admin_isactive_article_category,
         name="admin_isactive_article_category"),
    path('admin/makale-kategorileri/sil/<slug:slug>', article.admin_delete_article_category,
         name="admin_delete_article_category"),
    path('admin/makaleler/makale-kategorileri/ekle/', article.admin_add_article_category,
         name="admin_add_article_category"),
    # path('makaleler/makale-kategorileri/duzenle/<slug:slug>', article.admin_edit_article_category,
    #      name="admin_edit_article_category"),
    # path('makaleler/makale-kategorileri/sil/<slug:slug>', article.admin_delete_article_category,
    #      name="admin_delete_article_category"),

    # Social Media
    path('admin/sosyal-medya/', socialmedia.admin_all_social_medias, name="admin_all_social_medias"),
    path('admin/sosyal-medya/ekle', socialmedia.admin_add_social_media, name="admin_add_social_media"),
    path('admin/sosyal-medya/duzenle/<slug:slug>', socialmedia.admin_edit_social_media,
         name="admin_edit_social_media"),
    path('admin/sosyal-medya/isactive/<slug:slug>', socialmedia.admin_isactive_socialmedia,
         name="admin_isactive_socialmedia"),
    path('admin/sosyal-medya/sil/<slug:slug>', socialmedia.admin_delete_socialmedia,
         name="admin_delete_socialmedia"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
