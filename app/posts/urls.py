from django.urls import path

from posts.apis import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListCreateGenericAPIView.as_view(), name='list_create'),
    path('<int:pk>/', views.PostRetrieveUpdateDestroyGenericAPIView.as_view(),
         name='retrieve_update_destroy'),
    path('<int:pk>/like/', views.PostLikeToggleAPIView.as_view(),
         name='like'),
    path('category/', views.PostCategoryListGenericAPIView.as_view(), name='category'),
]
