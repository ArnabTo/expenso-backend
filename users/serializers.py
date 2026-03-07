from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    """Custom user creation serializer requiring password re-type."""
    re_password = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 're_password', 'currency')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('re_password', None):
            raise serializers.ValidationError({'re_password': 'Passwords do not match.'})
        return attrs


class UserSerializer(BaseUserSerializer):
    """Serializer for reading user profile."""
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'currency', 'bio', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')
