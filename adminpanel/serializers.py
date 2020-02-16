from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'description', 'groups', 'is_active',
                  'is_superuser', 'image']
