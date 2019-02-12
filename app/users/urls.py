from django.urls import path

from users.apis import views

app_name = 'users'

urlpatterns = [
    path('', views.UserCreateGenericAPIView.as_view(), name='create'),
    path('me/', views.UserProfileRetrieveUpdateDestroyGenericAPIView.as_view(), name='me-profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('following/<str:user_id>/', views.UserFollowingCreateListAPIView.as_view(), name='following'),
    path('follower/<str:user_id>/', views.UserFollowerListAPIView.as_view(), name='follower'),
    path('<str:user_id>/', views.UserProfileRetrieveGenericAPIView.as_view(), name='profile'),
]
