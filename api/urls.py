from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from ankadescankaya import settings
from api.views.v1.account import AccountRegistrationView, AccountLoginAPIView
from api.views.v1.article import ArticleLikeAPIToggle, ArticleDetailAPIToggle, ArticleListAPIView
from api.views.v1.group import IsActiveGroupAPIToggle
from api.views.v1.question import QuestionLikeAPIToggle, QuestionDetailAPIToggle, QuestionListAPI

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
app_name = "api"
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='ankades')),
    url(r'^', include(router.urls)),

    # Account
    url(r'^Account/Group/(?P<slug>[\w-]+)/IsActive/$', IsActiveGroupAPIToggle.as_view(), name="group-active-api-toggle"),
    url(r'^Account/Login/$', AccountLoginAPIView.as_view(), name="login-api"),
    url(r'^Account/Register/', AccountRegistrationView.as_view()),

    # Question
    url(r'^Question/(?P<slug>[\w-]+)/(?P<postNumber>[\w-]+)/Like/$', QuestionLikeAPIToggle.as_view(), name="question-like-api-toggle"),
    url(r'^Question/List/$', QuestionListAPI.as_view()),
    url(r'^Question/Detail/(?P<postNumber>[\w-]+)/$', QuestionDetailAPIToggle.as_view(),
        name="question-detail"),


    # Article
    url(r'^Article/List/$', ArticleListAPIView.as_view(), name="article-list"),
    url(r'^Article/(?P<username>[\w-]+)/(?P<slug>[\w-]+)/Like/$', ArticleLikeAPIToggle.as_view(), name="article-like-api-toggle"),
    url(r'^Article/(?P<postNumber>[\w-]+)/(?P<slug>[\w-]+)$', ArticleDetailAPIToggle.as_view(),
        name="article-detail-api"),

]
urlpatterns += router.urls
