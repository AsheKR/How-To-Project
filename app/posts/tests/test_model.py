import pytest
from django.contrib.auth import get_user_model

from posts.models import PostCategory, Post


class TestPostModel:

    def setup_method(self, method):
        self.user = get_user_model().objects.create(
            user_id='test123',
            password='P@ssw0rd',
            email='email@email.com',
        )
        self.category = PostCategory.objects.create(name='category1')

    def test_required_fields(self, django_user_model):
        post_info = (
            ('author', self.user),
            ('category', self.category),
            ('title', 'title1'),
            ('content', 'content'),
        )
        test_fields = dict()

        for field_name, field_value in post_info:
            with pytest.raises(TypeError) as e:
                django_user_model.objects.create_user(
                    **test_fields,
                )
            test_fields[field_name] = field_value

        post = Post.objects.create(
            **test_fields
        )

        assert post == Post.objects.first()

    def test_delete_generates_deleted_at(self):
        post_info = (
            ('author', self.user),
            ('category', self.category),
            ('title', 'title1'),
            ('content', 'content'),
        )

        post = Post.objects.create(
            **dict(post_info),
        )

        assert not post.deleted_at
        post.delete()
        assert post.deleted_at
