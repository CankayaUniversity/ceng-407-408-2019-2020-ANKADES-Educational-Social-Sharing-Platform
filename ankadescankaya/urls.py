from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

# from account.views import AccountViewSet, AccountActivityViewSet
# from adminpanel.views import AccountGroupsViewSet, AccountPermissionsViewSet, AdminActivityViewSet
# from course.views import CourseViewSet, CourseSubToSubCategoryViewSet, CourseCategoryViewSet

router = routers.SimpleRouter()
#Account API
# router.register('Account', AccountViewSet, "account")
# router.register('Account/Groups', AccountGroupsViewSet, "accountGroups")
# router.register('Account/Permissions', AccountPermissionsViewSet, "accountPermissions")
#
# #Course API
# router.register('Course', CourseViewSet, 'course')
# router.register('Course/Category', CourseCategoryViewSet, 'courseCategory')
# router.register('Course/SubToSub/Category', CourseSubToSubCategoryViewSet, 'courseSubToSubCategory')
#
# router.register('Activity/Admin', AdminActivityViewSet, 'activityAdmin')
# router.register('Activity/Account', AccountActivityViewSet, 'activityAccount')

schema_view = get_schema_view(
   openapi.Info(
      title="Ankades",
      default_version='v1',
      description="ANKADES API DOC",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="info@ankades.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('ankades-admin-panel/', include("adminpanel.urls")), #include ankades admin panel applications url
    path('', include("account.urls")), #include ankades account
    # path('', include("question.urls")), #include ankades question applications url
    # path('makaleler/', include("article.urls")), #include ankades article applications url
    # path('kullanici/', include("account.urls")), #include ankades account applications url
    # path('cikmis-sorular/', include("exam.urls")), #include ankades pre-exam applications url

    # swagger
    url(r'^ankades-api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)