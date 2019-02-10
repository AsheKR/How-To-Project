from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from users.apis.serializers import UserCreateSerializer, UserLoginSerializer, UserProfileSerializer

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
