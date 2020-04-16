from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include

from account.views import views as account_view
from ankadescankaya import views as main_view

urlpatterns = [
    path('api/', include("api.urls")),
    path('admin/', include("adminpanel.urls")),
    path('', include("account.urls")),
    path('', include("course.urls")),
    path('', include("question.urls")),
    path('', include("article.urls")),
    path('', include("exam.urls")),
    path('', include("directmessage.urls")),
    path('404', main_view.get_404, name="404"),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<username>[\w-]+)/$', account_view.account_detail, name="account_detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
