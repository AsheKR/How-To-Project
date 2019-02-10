from django.urls import path

from users.apis import views

app_name = 'users'

urlpatterns = [
    path('', views.UserCreateGenericAPIView.as_view(), name='create'),
    path('<int:pk>/', views.UserProfileGenericAPIView.as_view(), name='profile'),
    path('me/', views.UserProfileGenericAPIView.as_view(), name='me-profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('following/<int:to_user_pk>/', views.UserFollowingCreateListAPIView.as_view(), name='following'),
    path('follower/<int:from_user_pk>/', views.UserFollowerListAPIView.as_view(), name='follower'),
]
