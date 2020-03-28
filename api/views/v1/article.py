from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from article.models import Article


class ArticleLikeAPIToggle(APIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(operation_summary="Like an article by given a slug")
    def get(self, request, slug=None, format=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Article, slug=slug)
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