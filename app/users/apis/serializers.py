from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'user_id',
            'password',
            'email',
            'nickname',
            'profile_image',
        )

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
