from django.contrib import messages
from django.shortcuts import render, redirect

from account.models import Account, AccountFollower
from account.views.views import current_user_group, get_user_follower
from article.models import Article
from course.models import Course
from question.models import Question


def my_posts(request):
    """
    :param request:
    """
    try:
        instance = Account.objects.get(username=request.user)
        myCourses = Course.objects.filter(creator=request.user)
        myQuestions = Question.objects.filter(creator=request.user)
        myArticles = Article.objects.filter(creator=request.user)
        userGroup = current_user_group(request, request.user)
        existFollower = get_user_follower(request, request.user, instance)
        followers = AccountFollower.objects.filter(followingId__username=instance.username)
        followings = AccountFollower.objects.filter(followerId__username=instance.username)
        context = {
            "myCourses": myCourses,
            "myArticles": myArticles,
            "myQuestions": myQuestions,
            "userGroup": userGroup,
            "instance": instance,
            "existFollower": existFollower,
            "followers": followers,
            "followings": followings,
        }
        return render(request, "ankades/account/posts/my-posts.html", context)
    except:
        messages.error(request, "Giriş yapmalısınız.")
        return redirect("login_account")