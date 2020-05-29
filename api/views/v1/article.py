from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, permissions, status
from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from account.models import Account
from ankadescankaya.views.views import current_user_group
from api.serializer.serializers import ArticleSerializer
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


class ArticleDetailAPIToggle(APIView):

    @swagger_auto_schema(operation_summary="Get article by given slug and postNumber")
    def get(self, request, postNumber=None, slug=None, format=None):
        postNumber = self.kwargs.get("postNumber")
        slug = self.kwargs.get("slug")
        try:
            article = Article.objects.get(slug=slug, postNumber=postNumber)
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': None,
                'data': {'title': article.title, "postNumber": article.postNumber, 'slug': article.slug,
                         'isActive': article.isActive, 'view': article.view, 'category': article.categoryId.title,
                         'media': article.media.url, 'description': article.description}
            }
            status_code = status.HTTP_200_OK
        except:
            response = {
                'success': 'False',
                'status code': status.HTTP_404_NOT_FOUND,
                'message': 'Makale bulunamadı.',
                'data': None
            }
            status_code = status.HTTP_404_NOT_FOUND
        return Response(response, status=status_code)


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
