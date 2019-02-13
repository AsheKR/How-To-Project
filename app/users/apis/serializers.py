import re

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from users.models import UserRelation


class UserCreateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'user_id',
            'password',
            'email',
            'nickname',
        )

    def validate_user_id(self, value):
        if value[0].isdigit():
            self.register_error(error_message='user_id should not begin with number.',
                                error_code='2013',
                                field_name='user_id')

        if not value.islower():
            self.register_error(error_message='user_id must lowercase.',
                                error_code='2013',
                                field_name='user_id')

        if re.findall(r'[()[\]{}|\\`~!@#$%^&*\+=;:\'",<>./?]', value):
            self.register_error(error_message='user_id allow special character only "-" and "_"',
                                error_code='2013',
                                field_name='user_id')

        if len(value) < 5:
            self.register_error(error_message='user_id must at least 5 characters long.',
                                error_code='2051',
                                field_name='user_id')

        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def create(self, validated_data):
        self.user = get_user_model().objects.create_user(**validated_data)
        return self.user

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        return {
            'token': token.key,
        }


class UserLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(user_id=attrs['user_id'], password=attrs['password'])

        if not self.user:
            raise serializers.ValidationError({'detail': '유저 정보가 잘못되었습니다.'})
        return attrs

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        return {
            'token': token.key,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = (
            'password',
            'deleted_at',
        )
        read_only_fields = (
            'email',
            'user_id',
        )


class UserRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelation
        exclude = (
            'deleted_at',
        )
