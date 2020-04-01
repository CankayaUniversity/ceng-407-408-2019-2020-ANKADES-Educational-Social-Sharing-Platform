from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.views.views import current_user_group, user_articles, user_questions
from article.models import ArticleComment
from question.models import QuestionComment


def user_posts(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    if currentUser.is_authenticated:
        articles = user_articles(request, currentUser)
        questions = user_questions(request, currentUser)
        articleComments = ArticleComment.objects.filter(articleId__creator=currentUser)
        questionComments = QuestionComment.objects.filter(questionId__creator=currentUser)
        context = {
            "currentUser": currentUser,
            "userGroup": userGroup,
            "articles": articles,
            "questions": questions,
            "articleComments": articleComments,
            "questionComments": questionComments,
        }
        return render(request, "ankades/account/posts/user-posts.html", context)
    else:
        messages.error(request, "Öncelikle giriş yapmalısınız.")
        return redirect("index")