from django.contrib.auth import login, authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, authentication, permissions, viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.models import Account, AccountGroup
from api.serializers.account import RegisterSerializer, LoginSerializer, UserSerializer


class AccountRegistrationView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="Registration a new user")
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': None,
        }

        return Response(response, status=status_code)


class AccountLoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_summary="Login account")
    def post(self, request, username=None, password=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success': 'True',
            'status code': status.HTTP_200_OK,
            'message': None,
            'token': serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
