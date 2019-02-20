from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from base.base_error_mixins import NotRequireSerializerFriendlyErrorMessagesMixin
from posts.apis.filters import PostFilter
from posts.apis.permissions import PostUpdateDestroyMustBeOwner
from posts.apis.serializers import PostCategorySerializer, PostSerializer, PostCommentSerializer
from posts.models import PostCategory, Post, PostComment


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


class PostCommentListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = PostComment.objects.filter(deleted_at=None)
    serializer_class = PostCommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(post__pk=self.kwargs.get('pk'))
        return queryset


class PostCommentUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostComment.objects.filter(deleted_at=None, post__deleted_at=None)
    serializer_class = PostCommentSerializer
    permission_classes = (
        PostUpdateDestroyMustBeOwner,
    )

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            'post__pk': self.kwargs.get('post_pk'),
        }
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class PostLikeToggleAPIView(NotRequireSerializerFriendlyErrorMessagesMixin, APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.filter(deleted_at=None), pk=kwargs.get('pk'))
        if post.author == request.user:
            self.register_error_403(error_message='자신의 포스트에는 좋아요를 누를 수 없습니다.',
                                    error_code='1101',
                                    field_name='like')
        status = post.like_toggle(request.user)
        return Response(status=status)
