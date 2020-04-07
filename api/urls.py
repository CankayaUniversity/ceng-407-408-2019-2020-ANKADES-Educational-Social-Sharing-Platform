from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from ankadescankaya import settings
from api.views.v1.account import AccountRegistrationView, AccountLoginAPIView, FollowAccountAPI
from api.views.v1.article import ArticleLikeAPIToggle
from api.views.v1.group import IsActiveGroupAPIToggle
from api.views.v1.question import QuestionLikeAPIToggle

router = routers.SimpleRouter()

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
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='ankades')),
    url(r'^', include(router.urls)),
    # url(r'^Account/(?P<username>[\w-]+)/Follow/$', FollowAccountAPIToggle.as_view(), name="follow-api-toggle"),
    url(r'^Article/(?P<username>[\w-]+)/(?P<slug>[\w-]+)/Like/$', ArticleLikeAPIToggle.as_view(), name="article-like-api-toggle"),
    url(r'^Account/Group/(?P<slug>[\w-]+)/IsActive/$', IsActiveGroupAPIToggle.as_view(), name="group-active-api-toggle"),
    url(r'^Account/Follow/(?P<username>[\w-]+)/$', FollowAccountAPI.as_view(), name="follow-api"),
    url(r'^Account/Login/$', AccountLoginAPIView.as_view(), name="login-api"),

    # url(r'^Account/Profile/', UserProfileView.as_view()),
    url(r'^Account/Register/', AccountRegistrationView.as_view()),
    # url(r'^Account/Group/', AccountGroupView.as_view()),

    # Question
    url(r'^Question/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/Like/$', QuestionLikeAPIToggle.as_view(),
        name="question-like-api-toggle"),
]
urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
