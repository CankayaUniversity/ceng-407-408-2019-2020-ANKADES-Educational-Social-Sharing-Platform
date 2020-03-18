# from django.db.models import Q
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework import status, viewsets, authentication, permissions
# from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#
# from account.models import Account
# from account.serializers import UserRegistrationSerializer, UserLoginSerializer
#
#
# class UserRegistrationView(CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     permission_classes = (AllowAny,)
#
#     @swagger_auto_schema(operation_summary="Registration a new user")
#     def post(self, request, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         status_code = status.HTTP_201_CREATED
#         response = {
#             'success': 'True',
#             'status code': status_code,
#             'message': None,
#         }
#
#         return Response(response, status=status_code)
#
#
# class UserLoginView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer
#
#     @swagger_auto_schema(operation_summary="Login account")
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success': 'True',
#             'status code': status.HTTP_200_OK,
#             'message': None,
#             'token': serializer.data['token'],
#         }
#         status_code = status.HTTP_200_OK
#
#         return Response(response, status=status_code)
#
#
# class AccountGroupView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = AccountGroupSerializer
#
#     def get(self, request):
#         try:
#             user_profile = Account.objects.filter(Q(is_active=True))
#             status_code = status.HTTP_200_OK
#             response = {
#                 'data': [{
#                     'first_name': user_profile.username
#                 }]
#             }
#
#         except Exception as e:
#             status_code = status.HTTP_400_BAD_REQUEST
#             response = {
#                 'success': 'false',
#                 'status code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'User does not exists',
#                 'error': str(e)
#             }
#         return Response(response, status=status_code)
#
#
# class UserProfileView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     authentication_class = JSONWebTokenAuthentication
#
#     @swagger_auto_schema(operation_summary="Get Account")
#     def get(self, request, username):
#         try:
#             user_profile = Account.objects.get(username=request.user.username)
#             status_code = status.HTTP_200_OK
#             response = {
#                 'success': 'true',
#                 'status code': status_code,
#                 'message': 'User profile fetched successfully',
#                 'data': [{
#                     'first_name': user_profile.first_name,
#                     'last_name': user_profile.last_name,
#                     'date_joined': user_profile.date_joined,
#                     'is_active': user_profile.is_active,
#                     'image': user_profile.image,
#                     'description': user_profile.description,
#                 }]
#             }
#
#         except Exception as e:
#             status_code = status.HTTP_400_BAD_REQUEST
#             response = {
#                 'success': 'false',
#                 'status code': status.HTTP_400_BAD_REQUEST,
#                 'message': 'User does not exists',
#                 'error': str(e)
#             }
#         return Response(response, status=status_code)
#
#
# class AccountGroupViewSet(viewsets.ModelViewSet):
#     queryset = AccountGroup.objects.all()
#     serializer_class = AccountGroupSerializer
#
#
# class FollowAccountAPIToggle(APIView):
#     authentication_classes = (authentication.BasicAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#
#     @swagger_auto_schema(operation_summary="Follow an account by given username")
#     def get(self, request, username=None, format=None):
#         username = self.kwargs.get("username")
#         obj = get_object_or_404(Account, username=username)
#         user = self.request.user
#         updated = False
#         followed = False
#         if user.is_authenticated():
#             if user in obj.follower.all():
#                 followed = False
#                 obj.follower.remove(user)
#             else:
#                 followed = True
#                 obj.follower.add(user)
#             updated = True
#         data = {
#             "updated": updated,
#             "followed": followed
#         }
#         return Response(data)