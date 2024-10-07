from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):

    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    isActive = serializers.BooleanField(source='is_active')
    supabaseId = serializers.CharField(source='supabase_id')

    class Meta:
        model = User
        fields = [
            'id',
            'supabaseId',
            'email',
            'firstName',
            'lastName',
            'isActive'
        ]
        read_only_fields = ['id', 'supabaseId', 'email', 'isActive']


class UserCreateSerializer(serializers.ModelSerializer):

    supabaseId = serializers.UUIDField(source='supabase_id')

    class Meta:
        model = User
        fields = [
            'email',
            'supabaseId'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            user = User.objects.create(**validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return user
