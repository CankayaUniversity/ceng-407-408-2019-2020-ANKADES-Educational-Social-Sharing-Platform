from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from article.api_view import ArticleLikeAPIToggle
from directmessage import views
from directmessage.views import LikeDirectMessage

urlpatterns = [
    url(r'^(?P<username>\w+)/mesajlarim/$', views.my_direct_messages_list, name="my_direct_messages_list"),
    url(r'^mesaj-gonder/(?P<username>\w+)/$', views.send_direct_message, name="send_direct_message"),
    url(r'^mesaj/(?P<username>\w+)/$', views.direct_message_detail, name="direct_message_detail"),
    path('mesaj/<int:messageNumber>/engelle/', views.block_direct_message, name="block_direct_message"),
    path('mesaj/<int:messageNumber>/sil/', views.delete_direct_message, name="delete_direct_message"),
    url(r'^(?P<id>[\w-]+)/begen/$', LikeDirectMessage.as_view(), name="like-message"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)