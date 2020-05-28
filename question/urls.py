from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from question.views import views
from question.views.views import QuestionLikeToggle, QuestionLikeCommentToggle, QuestionAnswerVoteToggle

urlpatterns = [
    path('sorular/', views.all_questions, name="all_questions"),
    path('soru-sor/', views.add_question, name="add_question"),
    path('sorular/kategoriler/<slug:slug>', views.question_category_page, name="question_category_page"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<postNumber>[\w-]+)/$', views.question_detail, name="question_detail"),
    url(r'^(?P<postNumber>[\w-]+)/sikayet-et/$', views.add_report_question, name="add_report_question"),
    url(r'^cevap/(?P<answerNumber>[\w-]+)/onayla/$', views.confirm_answer, name="confirm_answer"),
    url(r'^soru-duzenle/(?P<postNumber>[\w-]+)/$', views.edit_question, name="edit_question"),
    url(r'^soru-sil/(?P<postNumber>[\w-]+)/sil/$', views.delete_question, name="delete_question"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<postNumber>[\w-]+)/yorum-yap/$', views.add_question_answer,
        name="add_question_answer"),
    url(r'^cevap/(?P<answerNumber>[\w-]+)/cevapla/$', views.add_question_answer_reply,
        name="add_question_answer_reply"),
    url(r'^soru/(?P<slug>[\w-]+)/(?P<postNumber>[\w-]+)/begen/$', QuestionLikeToggle.as_view(),
        name="question-like-toggle"),
    url(r'^cevap/(?P<answerNumber>[\w-]+)/begen/$', QuestionLikeCommentToggle.as_view(),
        name="question-like-comment-toggle"),
    url(r'^cevap/(?P<answerNumber>[\w-]+)/oyla/$', views.question_vote_comment,
        name="question_vote_comment"),
    url(r'^delete-answer/(?P<answerNumber>[\w-]+)/$', views.delete_question_answer, name="delete_question_answer"),
    url(r'^edit-answer/(?P<answerNumber>[\w-]+)/$', views.edit_question_answer, name="edit_question_answer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
