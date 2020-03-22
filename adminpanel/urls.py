from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from adminpanel.views import group, socialmedia, activity
from adminpanel.views import views, account, article
from adminpanel.views.group import IsActiveGroupToggle, IsActiveGroupAPIToggle

urlpatterns = [
    # Main Url
    path('admin/', views.admin_dashboard, name="admin_dashboard"),
    path('admin/login/', views.login_admin, name="login_admin"),
    path('admin/logout/', views.logout_admin, name="logout_admin"),
    # path('admin/add-new-user', account.admin_register_account, name="admin_register_account"),

    # User
    url(r'^admin/edit-profile/(?P<username>\w+)/$', account.admin_edit_profile, name="admin_edit_profile"),
    path('admin/groups/', account.admin_all_users, name="admin_all_users"),
    path('admin/user-groups', account.admin_all_user_groups, name="admin_all_user_groups"),
    path('admin/blocked-users', account.admin_blocked_users, name="admin_blocked_users"),
    url(r'^admin/profile/(?P<username>[\w-]+)/$', account.admin_my_account, name="admin_my_account"),
    url(r'^admin/block-user/(?P<username>\w+)/$', account.admin_block_account, name="admin_block_account"),
    url(r'^admin/students/', account.admin_students, name="admin_students"),
    url(r'^admin/teachers/', account.admin_teachers, name="admin_teachers"),
    url(r'^admin/moderators/', account.admin_moderators, name="admin_moderators"),
    url(r'^admin/admins/', account.admin_admins, name="admin_admins"),

    # User Permission
    # path('admin/account-permissions/', account.admin_account_permission, name="admin_account_permission"),
    # path('admin/add-account-permission/', account.admin_add_account_permission,
    #      name="admin_add_account_permission"),
    # path('admin/edit-account-permission/<uuid:id>', account.admin_edit_account_permission,
    #      name="admin_edit_account_permission"),
    # path('admin/delete-account-permission/<uuid:id>', account.admin_deactivate_account_permission,
    #      name="admin_deactivate_account_permission"),

    # User Group
    # path('kullanicilar/grup/', group.admin_account_groups, name="admin_account_groups"),
    # path('kullanicilar/grup/ekle/', account.admin_add_account_group, name="admin_add_account_group"),
    # path('kullanicilar/grup/duzenle/<uuid:id>', account.admin_edit_account_group, name="admin_edit_account_group"),
    # path('kullanicilar/grup/sil/<uuid:id>', group.admin_delete_account_group, name="admin_delete_account_group"),

    # Group
    path('admin/all-groups/', group.admin_all_groups, name="admin_all_groups"),
    path('admin/add-group/', group.admin_add_group, name="admin_add_group"),
    path('admin/edit-group/<slug:slug>/', group.admin_edit_group, name="admin_edit_group"),
    url(r'^admin/grup/sil/(?P<slug>\w+)/$', group.admin_delete_group,
        name="admin_delete_group"),
    path('admin/isactive-group/<slug:slug>', group.admin_isactive_group,
         name="admin_isactive_group"),

    url(r'^admin/toggle/isactive-group/(?P<slug>[\w-]+)/$', IsActiveGroupToggle.as_view(), name="active-toggle"),
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
    path('admin/articles/', article.admin_all_articles, name="admin_all_articles"),
    path('admin/add-article/', article.admin_add_article, name="admin_add_article"),
    path('admin/isactive-article/<slug:slug>/', article.admin_isactive_article, name="admin_isactive_article"),
    path('admin/delete-article/<slug:slug>/', article.admin_delete_article, name="admin_delete_article"),
    # path('makale/<slug:slug>/duzenle/', article.admin_edit_article, name="admin_edit_article"),

    # Tag
    path('admin/tags/', views.admin_tags, name="admin_tags"),
    path('admin/add-tag', views.admin_add_tag, name="admin_add_tag"),
    # path('etiketler/duzenle/<slug:slug>', article.admin_edit_tag, name="admin_edit_tag"),
    # path('etiketler/sil/<slug:slug>', article.admin_delete_tag, name="admin_delete_tag"),
    #

    # Article Category
    path('admin/article-categories/', article.admin_article_categories, name="admin_article_categories"),
    path('admin/isactive-article-categories<slug:slug>/', article.admin_isactive_article_category,
         name="admin_isactive_article_category"),
    path('admin/delete-article-category/<slug:slug>/', article.admin_delete_article_category,
         name="admin_delete_article_category"),
    path('admin/add-article-category/', article.admin_add_article_category,
         name="admin_add_article_category"),
    # path('makaleler/makale-kategorileri/duzenle/<slug:slug>', article.admin_edit_article_category,
    #      name="admin_edit_article_category"),
    # path('makaleler/makale-kategorileri/sil/<slug:slug>', article.admin_delete_article_category,
    #      name="admin_delete_article_category"),

    # Social Media
    path('admin/social-medias/', socialmedia.admin_all_social_medias, name="admin_all_social_medias"),
    path('admin/add-social-media/', socialmedia.admin_add_social_media, name="admin_add_social_media"),
    path('admin/edit-social-media/<slug:slug>/', socialmedia.admin_edit_social_media,
         name="admin_edit_social_media"),
    path('admin/isactive-social-media/<slug:slug>/', socialmedia.admin_isactive_socialmedia,
         name="admin_isactive_socialmedia"),
    path('admin/delete-social-media/<slug:slug>/', socialmedia.admin_delete_socialmedia,
         name="admin_delete_socialmedia"),

    # Admin Log Urls
    path('admin/logs/', activity.admin_all_logs, name="admin_all_logs"),
    path('admin/logs/admins', activity.admin_admin_logs, name="admin_admin_logs"),
    path('admin/logs/accounts', activity.admin_account_logs, name="admin_account_logs"),
    path('admin/logs/admin/delete-log/<uuid:id>/', activity.admin_delete_admin_log, name="admin_delete_admin_log"),
    path('admin/logs/accounts/delete-log/<uuid:id>/', activity.admin_delete_account_log, name="admin_delete_account_log"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
