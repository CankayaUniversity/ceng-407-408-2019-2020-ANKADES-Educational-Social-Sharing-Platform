from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

router = routers.SimpleRouter()
# router.register('Permission', PermissionViewSet, "permission")
# router.register('Group', GroupViewSet, "group")
# router.register('Account', AccountViewSet, "account")
# router.register('AccountPermission', AccountPermissionViewSet, "accountPermission")
# router.register('GroupPermission', GroupPermissionViewSet, "groupPermission")
# router.register('AccountGroup', AccountGroupViewSet, "accountGroup")
# router.register('AccountActivity', AccountActivityViewSet, "accountActivity")
# router.register('AdminActivity', AdminActivityViewSet, "adminActivity")
# router.register('School', SchoolViewSet, "school")


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
    path('admin/', include("adminpanel.urls")),
    path('', include("account.urls")),
    path('', include("course.urls")),
    path('', include("article.urls")),
    path('', include("exam.urls")),
    path('', include("directmessage.urls")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # swagger
    url(r'^ankades-api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
