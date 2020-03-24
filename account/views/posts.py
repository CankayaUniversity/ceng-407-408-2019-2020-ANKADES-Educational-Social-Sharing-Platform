from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from account.models import Account
from account.views.views import current_user_group, user_articles, article_comment_count
from article.models import ArticleComment


def user_posts(request):
    currentUser = request.user
    userGroup = current_user_group(request, currentUser)
    articles = user_articles(request, currentUser)
    articleComments = ArticleComment.objects.filter(articleId__creator=currentUser)
    context = {
        "currentUser": currentUser,
        "userGroup": userGroup,
        "articles": articles,
    }
    return render(request, "ankades/account/posts/user-posts.html", context)