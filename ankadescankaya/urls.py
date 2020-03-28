from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include

from account.views import user
from account.views.views import FollowAccountToggle

urlpatterns = [
    path('api/', include("api.urls")),
    path('admin/', include("adminpanel.urls")),
    path('', include("account.urls")),
    path('', include("course.urls")),
    path('', include("article.urls")),
    path('', include("exam.urls")),
    path('', include("directmessage.urls")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<username>[\w-]+)/$', user.account_detail, name="account_detail"),
    url(r'^(?P<username>[\w-]+)/takip/$', FollowAccountToggle.as_view(), name="follow-toggle"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
