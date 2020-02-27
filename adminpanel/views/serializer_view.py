from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from account.models import Permission, Group, Account, AccountPermission, GroupPermission, AccountGroup, AccountActivity
from adminpanel.models import AdminActivity
from adminpanel.serializers import AccountSerializer, GroupSerializer, AccountGroupSerializer, PermissionSerializer, \
    AccountPermissionSerializer, GroupPermissionSerializer, AccountActivitySerializer, AdminActivitySerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('-date_joined')
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-createdDate')
    serializer_class = GroupSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer


class AccountPermissionViewSet(viewsets.ModelViewSet):
    queryset = AccountPermission.objects.all().order_by('-createdDate')
    serializer_class = AccountPermissionSerializer


class GroupPermissionViewSet(viewsets.ModelViewSet):
    queryset = GroupPermission.objects.all().order_by('-createdDate')
    serializer_class = GroupPermissionSerializer


class AccountGroupViewSet(viewsets.ModelViewSet):
    queryset = AccountGroup.objects.all().order_by('-createdDate')
    serializer_class = AccountGroupSerializer


class AccountActivityViewSet(viewsets.ModelViewSet):
    queryset = AccountActivity.objects.all().order_by('-activityCreatedDate')
    serializer_class = AccountActivitySerializer


class AdminActivityViewSet(viewsets.ModelViewSet):
    queryset = AdminActivity.objects.all().order_by('-activityCreatedDate')
    serializer_class = AdminActivitySerializer


# class IsLoggedInUserOrAdmin(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         return obj == request.user or request.user.is_superuser
#
#
# class IsAdminUser(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         perm = AccountPermission()
#         return request.user and request.user.is_superuser
#
#     def has_object_permission(self, request, view, obj):
#         return request.user and request.user.is_superuser


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [AllowAny]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsLoggedInUserOrAdmin]
#         elif self.action == 'list' or self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]
