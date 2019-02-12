from django.urls import path

from posts.apis import views

app_name = 'posts'

urlpatterns = [
    path('category/', views.PostCategoryListGenericAPIView.as_view(), name='category')
]
