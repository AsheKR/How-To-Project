from rest_framework import generics

from posts.apis.serializers import PostCategorySerializer
from posts.models import PostCategory


class PostCategoryListGenericAPIView(generics.ListAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
