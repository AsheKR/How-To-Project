from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework import generics, status, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users.apis.serializers import UserCreateSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserRelationSerializer
from users.models import UserRelation

User = get_user_model()


class UserCreateGenericAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted_at=None)

    def get_object(self):
        if not self.kwargs.get('pk'):
            self.kwargs['pk'] = self.request.user.pk
        return super().get_object()


class UserFollowingCreateListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(from_user_relation__to_user=kwargs.get('to_user_pk'),
                                       from_user_relation__deleted_at=None,
                                       )
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        obj, created = UserRelation.objects.get_or_create(
            from_user=request.user,
            to_user=get_object_or_404(User.objects.filter(deleted_at=None), pk=kwargs.get('to_user_pk')),
        )

        if not created:
            if obj.deleted_at:
                obj.deleted_at = None
                obj.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                obj.deleted_at = now()
                obj.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_201_CREATED)


class UserFollowerListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(to_user_relation__from_user=kwargs.get('from_user_pk'),
                                       to_user_relation__deleted_at=None,
                                       )
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)
