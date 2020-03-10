from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from account.models import Account, Group

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'date_joined', 'is_active', 'image', 'description')


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = Account
        fields = ('username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = Account.objects.create_user(**validated_data)
        Account.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            data_joined=profile_data['data_joined'],
            is_active=profile_data['is_active'],
            image=profile_data['image'],
            description=profile_data['description'],
        )
        return user


# class UserGroupSerializer(serializers.Serializer):
#     profile = UserSerializer(required=False)
#
#     class Meta:
#         model = Group
#         fields = ('title', 'slug', 'isActive')
#
#     @swagger_auto_schema(operation_summary="Get Account groups")
#     def validate(self, attrs):


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }
