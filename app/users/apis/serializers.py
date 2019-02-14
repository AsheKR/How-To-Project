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
            self.register_error(error_message='이 필드는 숫자로 시작하면 안됩니다.',
                                error_code='2013',
                                field_name='user_id')

        if not value.islower():
            self.register_error(error_message='이 필드는 반드시 소문자로 작성되어야합니다.',
                                error_code='2013',
                                field_name='user_id')

        if re.findall(r'[()[\]{}|\\`~!@#$%^&*\+=;:\'",<>./?]', value):
            self.register_error(error_message='유저 아이디에는 오직 "_"와 "-"만 허용합니다.',
                                error_code='2013',
                                field_name='user_id')

        if len(value) < 5:
            self.register_error(error_message='이 필드의 글자 수가 5자 이상인지 확인하십시오.',
                                error_code='2051',
                                field_name='user_id')

        return value

    def validate_password(self, value):
        if len(value) < 8:
            self.register_error(error_message='이 필드의 글자 수가 8자 이상인지 확인하십시오.',
                                error_code='2051',
                                field_name='password')

        if not re.search(r'\d', value):
            self.register_error(error_message='이 필드는 반드시 하나 이상의 숫자를 포함하여야 합니다.',
                                error_code='2013',
                                field_name='password')

        if not re.search(r'[A-Z]', value):
            self.register_error(error_message='이 필드는 반드시 A-Z까지의 대문자를 포함하여야 합니다.',
                                error_code='2013',
                                field_name='password')

        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*\+=;:\'",<>./?]', value):
            self.register_error(error_message='이 필드는 반드시 특수문자가 하나 이상 포함되어야 합니다.',
                                error_code='2013',
                                field_name='password')

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


class UserLoginSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(user_id=attrs['user_id'], password=attrs['password'])

        if not self.user:
            self.register_error(error_message='아이디 혹은 비밀번호가 잘못되었습니다.',
                                error_code='3021',
                                field_name='login_failed')
        return attrs

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        return {
            'token': token.key,
        }


class UserProfileSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'user_id',
            'email',
            'nickname',
            'description',
            'profile_image',
            'created_at',
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
