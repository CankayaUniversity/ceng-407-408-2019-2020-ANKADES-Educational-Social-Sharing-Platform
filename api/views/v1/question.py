from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, permissions
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from account.models import AccountFollower
from account.views.views import get_user_follower, user_articles, user_questions, user_courses, user_exams
from ankadescankaya.views.views import current_user_group
from api.serializer.serializers import QuestionSerializer
from question.models import Question, QuestionComment


class QuestionLikeAPIToggle(APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(operation_summary="Like an article by given a slug")
    def get(self, request, slug=None, postNumber=None, format=None):
        slug = self.kwargs.get("slug")
        postNumber = self.kwargs.get("postNumber")
        obj = get_object_or_404(Question, slug=slug, postNumber=postNumber)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


class QuestionDetailAPIToggle(APIView):

    @swagger_auto_schema(operation_summary="Get question by given slug and postNumber")
    def get(self, request, postNumber=None, format=None):
        postNumber = self.kwargs.get("postNumber")
        obj = get_object_or_404(Question, postNumber=postNumber)
        userGroup = current_user_group(request, request.user)
        data = {
            "title": obj.title,
            "description": obj.description,
            "slug": obj.slug,
            "postNumber": obj.postNumber,
            "creator": obj.creator.get_full_name(),
            "category": obj.categoryId.title,
            "isSolved": obj.isSolved,
            "isActive": obj.isActive,
            "createdDate": obj.createdDate,
            "updatedDate": obj.updatedDate,
            "view": obj.view,
            "likes": obj.likes.count(),
            "userGroup": userGroup,
        }
        return Response(data)


class QuestionListAPI(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.BasePermission, )
