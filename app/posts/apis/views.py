from rest_framework import generics, permissions

from posts.apis.serializers import PostCategorySerializer, PostSerializer
from posts.models import PostCategory, Post


class PostCategoryListGenericAPIView(generics.ListAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
