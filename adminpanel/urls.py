from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from adminpanel.views import group, socialmedia, activity
from adminpanel.views import views, account, article
from adminpanel.views.group import IsActiveGroupAPIToggle

urlpatterns = [
    # Main Url
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('login/', views.login_admin, name="login_admin"),
    path('logout/', views.logout_admin, name="logout_admin"),
    # path('add-new-user', account.admin_register_account, name="admin_register_account"),

    # User
    url(r'^edit-profile/(?P<username>\w+)/$', account.admin_edit_profile, name="admin_edit_profile"),
    path('all-users/', account.admin_all_users, name="admin_all_users"),
    path('user-groups', account.admin_all_user_groups, name="admin_all_user_groups"),
    path('blocked-users', account.admin_blocked_users, name="admin_blocked_users"),
    url(r'^profile/(?P<username>[\w-]+)/$', account.admin_my_account, name="admin_my_account"),
    url(r'^block-user/(?P<username>\w+)/$', account.admin_block_account, name="admin_block_account"),
    url(r'^students/', account.admin_students, name="admin_students"),
    url(r'^teachers/', account.admin_teachers, name="admin_teachers"),
    url(r'^members/', account.admin_members, name="admin_members"),
    url(r'^moderators/', account.admin_moderators, name="admin_moderators"),
    url(r'^admins/', account.admin_admins, name="admin_admins"),
    url(r'^register/', account.admin_register_account, name="admin_register_account"),

    # User Permission
    # path('account-permissions/', account.admin_account_permission, name="admin_account_permission"),
    # path('add-account-permission/', account.admin_add_account_permission,
    #      name="admin_add_account_permission"),
    # path('edit-account-permission/<uuid:id>', account.admin_edit_account_permission,
    #      name="admin_edit_account_permission"),
    # path('delete-account-permission/<uuid:id>', account.admin_deactivate_account_permission,
    #      name="admin_deactivate_account_permission"),

    # User Group
    # path('kullanicilar/grup/', group.admin_account_groups, name="admin_account_groups"),
    path('kullanicilar/grup/ekle/', account.admin_add_account_group, name="admin_add_account_group"),
    # path('kullanicilar/grup/duzenle/<uuid:id>', account.admin_edit_account_group, name="admin_edit_account_group"),
    # path('kullanicilar/grup/sil/<uuid:id>', group.admin_delete_account_group, name="admin_delete_account_group"),

    # Group
    path('groups/', group.admin_all_groups, name="admin_all_groups"),
    path('add-group/', group.admin_add_group, name="admin_add_group"),
    url(r'^groups/(?P<slug>[\w-]+)/edit-group/', group.admin_edit_group, name="admin_edit_group"),
    url(r'^groups/delete/(?P<slug>[\w-]+)/$', group.admin_delete_group,
        name="admin_delete_group"),
    path('isactive-group/<slug:slug>', group.admin_isactive_group,
         name="admin_isactive_group"),

    url(r'^AdminPanel/Group/(?P<slug>[\w-]+)/IsActive/$', IsActiveGroupAPIToggle.as_view(), name="active-api-toggle"),

    # Group Permission
    # path('gruplar/grup-izinleri/', group.admin_group_permission, name="admin_group_permission"),
    # path('gruplar/grup-izinleri/ekle', group.admin_add_group_permission, name="admin_add_group_permission"),
    # path('gruplar/grup-izinleri/sil/<uuid:id>', group.admin_delete_group_permission,
    #      name="admin_delete_group_permission"),
    # path('gruplar/grup-izinleri/duzenle/<uuid:id>', group.admin_edit_group_permission,
    #      name="admin_edit_group_permission"),
    #
    # Permission
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
    path('articles/', article.admin_all_articles, name="admin_all_articles"),
    path('add-article/', article.admin_add_article, name="admin_add_article"),
    path('isactive-article/<slug:slug>/', article.admin_isactive_article, name="admin_isactive_article"),
    path('delete-article/<slug:slug>/', article.admin_delete_article, name="admin_delete_article"),
    # path('makale/<slug:slug>/duzenle/', article.admin_edit_article, name="admin_edit_article"),

    # Tag
    path('tags/', views.admin_tags, name="admin_tags"),
    path('add-tag', views.admin_add_tag, name="admin_add_tag"),
    # path('etiketler/duzenle/<slug:slug>', article.admin_edit_tag, name="admin_edit_tag"),
    # path('etiketler/sil/<slug:slug>', article.admin_delete_tag, name="admin_delete_tag"),
    #

    # Article Category
    path('article-categories/', article.admin_article_categories, name="admin_article_categories"),
    path('isactive-article-categories<slug:slug>/', article.admin_isactive_article_category,
         name="admin_isactive_article_category"),
    path('delete-article-category/<slug:slug>/', article.admin_delete_article_category,
         name="admin_delete_article_category"),
    path('add-article-category/', article.admin_add_article_category,
         name="admin_add_article_category"),
    # path('makaleler/makale-kategorileri/duzenle/<slug:slug>', article.admin_edit_article_category,
    #      name="admin_edit_article_category"),
    # path('makaleler/makale-kategorileri/sil/<slug:slug>', article.admin_delete_article_category,
    #      name="admin_delete_article_category"),

    # Social Media
    path('social-medias/', socialmedia.admin_all_social_medias, name="admin_all_social_medias"),
    path('add-social-media/', socialmedia.admin_add_social_media, name="admin_add_social_media"),
    path('edit-social-media/<slug:slug>/', socialmedia.admin_edit_social_media,
         name="admin_edit_social_media"),
    path('isactive-social-media/<slug:slug>/', socialmedia.admin_isactive_socialmedia,
         name="admin_isactive_socialmedia"),
    path('delete-social-media/<slug:slug>/', socialmedia.admin_delete_socialmedia,
         name="admin_delete_socialmedia"),

    # Admin Log Urls
    path('logs/', activity.admin_all_logs, name="admin_all_logs"),
    path('logs/admins', activity.admin_admin_logs, name="admin_admin_logs"),
    path('logs/accounts', activity.admin_account_logs, name="admin_account_logs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
