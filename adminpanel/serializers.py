# from django.contrib.auth.models import Group, Permission
# from rest_framework import serializers
#
# from account.models import Account
# from adminpanel.models import AdminActivity
#
#
# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'description', 'groups', 'is_active',
#                   'is_superuser', 'image']
#
#
# class AccountGroupsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']
#
#
# class AccountPermissionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = '__all__'
#
#
# class AdminActivitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdminActivity
#         fields = '__all__'