from rest_framework import serializers
from Auth.models import Credential, Token


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = ['username', 'password','url']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['access', 'refresh']