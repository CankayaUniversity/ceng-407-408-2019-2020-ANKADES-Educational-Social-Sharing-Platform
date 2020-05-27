from django.contrib import messages
from django.shortcuts import render, redirect

from account.models import Account, AccountFollower
from account.views.views import get_user_follower, user_articles, user_questions, user_courses, user_exams
from ankadescankaya.views.views import current_user_group, Categories
from article.models import Article
from course.models import Course
from question.models import Question, QuestionComment


def my_posts(request):
    """
    :param request:
    """
    try:
        instance = Account.objects.get(username=request.user)
    except:
        messages.error(request, "Bir sorun oluştu.")
        return redirect("404")
    followers = AccountFollower.objects.filter(followingId__username=instance.username)
    followings = AccountFollower.objects.filter(followerId__username=instance.username)
    getFollowerForFollow = get_user_follower(request, request.user, followers)
    getFollowingForFollow = get_user_follower(request, request.user, followings)
    articles = user_articles(request, request.user.username).order_by('-createdDate__day')
    questions = user_questions(request, request.user.username).order_by('-createdDate__day')
    courses = user_courses(request, request.user.username).order_by('-createdDate__day')
    exams = user_exams(request, request.user.username)
    certifiedAnswersCount = QuestionComment.objects.filter(creator=instance, isCertified=True, isActive=True)
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
        "getFollowerForFollow": getFollowerForFollow,
        "getFollowingForFollow": getFollowingForFollow,
        "articles": articles,
        "questions": questions,
        "courses": courses,
        "exams": exams,
        "certifiedAnswersCount": certifiedAnswersCount,
        "followers": followers,
        "followings": followings,
        "existFollower": existFollower,
    }
    return render(request, "ankades/account/posts/my-posts.html", context)