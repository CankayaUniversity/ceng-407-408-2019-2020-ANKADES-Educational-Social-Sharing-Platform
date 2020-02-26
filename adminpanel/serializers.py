from rest_framework import serializers, views
from rest_framework.decorators import api_view

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

