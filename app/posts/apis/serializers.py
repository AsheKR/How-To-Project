from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from posts.models import PostCategory, Post


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        exclude_fields = (
            'deleted_at',
        )
        read_only_fields = (
            'author',
            'category',
        )

    def create(self, validated_data):
        author = self.context.get('request').user
        category_name = self.context.get('request').data.get('category')
        category = get_object_or_404(PostCategory.objects.all(), name=category_name)

        instance = Post.objects.create(
            author=author,
            category=category,
            **validated_data
        )

        return instance
