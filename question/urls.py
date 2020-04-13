from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from question.views import views
from question.views.views import QuestionLikeToggle, QuestionLikeCommentToggle

urlpatterns = [
    path('sorular/', views.all_questions, name="all_questions"),
    path('soru-sor/', views.add_question, name="add_question"),
    path('sorular/kategoriler/<slug:slug>', views.question_category_page, name="question_category_page"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/$', views.question_detail, name="question_detail"),
    url(r'^cevap/(?P<id>[\w-]+)/onayla/$', views.confirm_answer, name="confirm_answer"),
    url(r'^(?P<id>[\w-]+)/sil/$', views.delete_answer, name="delete_answer"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/duzenle/$', views.edit_question, name="edit_question"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/yorum-yap/$', views.add_question_answer, name="add_question_answer"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/sil/$', views.delete_question, name="delete_question"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/like/$', QuestionLikeToggle.as_view(), name="question-like-toggle"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<questionNumber>[\w-]+)/like/$', QuestionLikeCommentToggle.as_view(), name="question-like-comment-toggle"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)