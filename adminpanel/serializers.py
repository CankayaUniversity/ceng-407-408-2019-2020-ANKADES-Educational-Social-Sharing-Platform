from rest_framework import serializers, views, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from account.models import Account, Group, AccountGroup, AccountPermission, Permission, GroupPermission, AccountActivity
from adminpanel.models import AdminActivity


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['title', 'slug', 'createdDate', 'updatedDate', 'isActive']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['title', 'slug', 'createdDate', 'updatedDate', 'isActive']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'is_active',
                  'is_superuser', 'image']


class AccountPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPermission
        fields = ['userId', 'permissionId', 'createdDate', 'updatedDate', 'isActive']


class GroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPermission
        fields = ['groupId', 'permissionId', 'createdDate', 'updatedDate', 'isActive']


class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = ['userId', 'groupId', 'isActive', 'createdDate', 'updatedDate']


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        fields = ['activityCreator', 'activityTitle', 'activityApplication', 'activityDescription', 'activityMethod', 'activityCreatedDate', 'activityUpdatedDate']


class AdminActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActivity
        fields = ['activityCreator', 'activityTitle', 'activityApplication', 'activityDescription', 'activityMethod', 'activityCreatedDate', 'activityUpdatedDate']


class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        perm = AccountPermission()
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser


class UserViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
