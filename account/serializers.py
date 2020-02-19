from rest_framework import serializers

from account.models import AccountActivity


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        fields = '__all__'
