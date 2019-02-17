from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from posts.models import PostCategory, Post


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'


class PostSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = (
            'deleted_at',
            'like_users',
        )
        read_only_fields = (
            'author',
            'like_users',
        )

    def create(self, validated_data):
        author = self.context.get('request').user

        instance = Post.objects.create(
            author=author,
            **validated_data
        )

        return instance
