from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from adminpanel.views import group, socialmedia, activity, question, permission, course, exam
from adminpanel.views import views, account, article

urlpatterns = [
    # Main Url
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('login/', views.login_admin, name="login_admin"),
    path('logout/', views.logout_admin, name="logout_admin"),

    # User
    path('all-users/', account.admin_all_users, name="admin_all_users"),
    path('all-active-users/', account.admin_active_users, name="admin_active_users"),
    path('user-groups/', account.admin_all_user_groups, name="admin_all_user_groups"),
    path('blocked-users/', account.admin_blocked_users, name="admin_blocked_users"),
    path('students/', account.admin_students, name="admin_students"),
    path('teachers/', account.admin_teachers, name="admin_teachers"),
    path('members/', account.admin_members, name="admin_members"),
    path('moderators/', account.admin_moderators, name="admin_moderators"),
    path('admins/', account.admin_admins, name="admin_admins"),
    path('register/', account.admin_register_account, name="admin_register_account"),

    url(r'^block-user/(?P<username>[\w-]+)/$', account.admin_block_account, name="admin_block_account"),
    url(r'^delete-user/(?P<username>[\w-]+)/$', account.admin_delete_account, name="admin_delete_account"),

    # User Group
    path('add-group-to-user/', account.admin_add_group_to_user, name="admin_add_group_to_user"),
    path('add-permission-to-user/', account.admin_add_permission_to_user, name="admin_add_permission_to_user"),

    # Group
    path('groups/', group.admin_all_groups, name="admin_all_groups"),
    path('add-group/', group.admin_add_group, name="admin_add_group"),
    url(r'^groups/(?P<slug>[\w-]+)/edit-group/$', group.admin_edit_group, name="admin_edit_group"),
    url(r'^groups/delete/(?P<slug>[\w-]+)/$', group.admin_delete_group,
        name="admin_delete_group"),
    path('isactive-group/<slug:slug>/', group.admin_isactive_group,
         name="admin_isactive_group"),

    # Question
    path('all-questions/', question.admin_all_questions, name="admin_all_questions"),
    url(r'^all-questions/active/(?P<slug>[\w-]+)/$', question.admin_isactive_question,
        name="admin_isactive_question"),
    url(r'^all-questions/delete/(?P<slug>[\w-]+)/$', question.admin_delete_question,
        name="admin_delete_question"),
    path('question-categories/', question.admin_question_categories, name="admin_question_categories"),
    path('isactive-question-categories/<slug:slug>/', question.admin_isactive_question_category,
         name="admin_isactive_question_category"),
    path('delete-question-category/<slug:slug>/', question.admin_delete_question_category,
         name="admin_delete_question_category"),
    path('add-question-category/', question.admin_add_question_category,
         name="admin_add_question_category"),


    # Course
    path('all-courses/', course.admin_all_courses, name="admin_all_courses"),
    url(r'^all-courses/active/(?P<slug>[\w-]+)/$', course.admin_isactive_course,
        name="admin_isactive_course"),
    url(r'^all-courses/delete/(?P<slug>[\w-]+)/$', course.admin_delete_course,
        name="admin_delete_course"),
    path('course-categories/', course.admin_course_categories, name="admin_course_categories"),
    path('isactive-course-categories/<slug:slug>/', course.admin_isactive_course_category,
         name="admin_isactive_course_category"),
    path('delete-course-category/<slug:slug>/', course.admin_delete_course_category,
         name="admin_delete_course_category"),


    # Course Category
    path('course-categories/', course.admin_course_categories, name="admin_course_categories"),
    url(r'^isactive-course-category/(?P<slug>[\w-]+)/$', course.admin_isactive_course_category,
        name="admin_isactive_course_category"),
    path('delete-course-category/<slug:slug>/', course.admin_delete_course_category,
         name="admin_delete_course_category"),
    path('add-course-category/', course.admin_add_course_category,
         name="admin_add_course_category"),


    # Permission
    path('permissions/', permission.admin_all_permissions, name="admin_all_permissions"),
    path('add-permission/', permission.admin_add_permission, name="admin_add_permission"),
    path('delete-permission/<slug:slug>/', permission.admin_delete_permission, name="admin_delete_permission"),
    path('isactive-permission/<slug:slug>/', permission.admin_isactive_permission, name="admin_isactive_permission"),

    # Article
    path('articles/', article.admin_all_articles, name="admin_all_articles"),
    path('isactive-article/<slug:slug>/', article.admin_isactive_article, name="admin_isactive_article"),
    path('delete-article/<slug:slug>/', article.admin_delete_article, name="admin_delete_article"),

    # Tag
    path('tags/', views.admin_tags, name="admin_tags"),
    path('add-tag/', views.admin_add_tag, name="admin_add_tag"),

    # Article Category
    path('article-categories/', article.admin_article_categories, name="admin_article_categories"),
    url(r'^isactive-article-category/(?P<slug>[\w-]+)/$', article.admin_isactive_article_category,
        name="admin_isactive_article_category"),
    path('delete-article-category/<slug:slug>/', article.admin_delete_article_category,
         name="admin_delete_article_category"),
    path('add-article-category/', article.admin_add_article_category,
         name="admin_add_article_category"),

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
    path('logs/admins/', activity.admin_admin_logs, name="admin_admin_logs"),
    path('logs/accounts/', activity.admin_account_logs, name="admin_account_logs"),

    #Exam
    path('okul-ekle/', exam.admin_add_school, name="admin_add_school"),
    path('bolum-ekle/', exam.admin_add_department, name="admin_add_department"),
    path('okullar/', exam.admin_all_schools, name="admin_all_schools"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
