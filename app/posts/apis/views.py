from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.apis.filters import PostFilter
from posts.apis.permissions import PostUpdateDestroyMustBeOwner
from posts.apis.serializers import PostCategorySerializer, PostSerializer
from posts.models import PostCategory, Post


class PostCategoryListGenericAPIView(generics.ListAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        return super().post(request, *args, **kwargs)


class PostRetrieveUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(deleted_at=None)
    serializer_class = PostSerializer
    permission_classes = (
        PostUpdateDestroyMustBeOwner,
    )


class PostLikeToggleAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.all(), pk=kwargs.get('pk'))
        status = post.like_toggle(request.user)
        return Response(status=status)
