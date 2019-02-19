from sqlite3 import IntegrityError

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from posts.models import PostCategory, Post, PostComment


class TestPostModel:

    def setup_method(self, method):
        self.user = get_user_model().objects.create_user(
            user_id='test123',
            password='P@ssw0rd',
            email='email@email.com',
            nickname='nickname',
        )
        self.category = PostCategory.objects.create(name='category1')

    def test_required_fields(self):
        post_info = (
            ('author', self.user),
            ('category', self.category),
            ('title', 'title1'),
            ('content', 'content'),
        )
        test_fields = dict()

        for field_name, field_value in post_info:
            with pytest.raises(ValidationError) as e:
                Post.objects.create(
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

    def test_post_like(self):
        post_info = (
            ('author', self.user),
            ('category', self.category),
            ('title', 'title1'),
            ('content', 'content'),
        )

        post = Post.objects.create(
            **dict(post_info),
        )

        assert post.like_users.count() == 0
        post.like_toggle(self.user)
        assert post.like_users.count() == 1
        post.like_toggle(self.user)
        assert post.like_users.count() == 0


class TestPostCommentModel:
    def setup_method(self, method):
        self.user = get_user_model().objects.create_user(
            user_id='test123',
            password='P@ssw0rd',
            email='email@email.com',
            nickname='nickname',
        )
        self.category = PostCategory.objects.create(name='category1')
        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title='title1',
            content='content',
        )

    def test_post_comment_require_fields(self):
        comment_info = (
            ('author', self.user),
            ('post', self.post),
            ('content', 'comment'),
        )
        test_fields = dict()

        for field_name, field_value in comment_info:
            with pytest.raises(ValidationError) as e:
                PostComment.objects.create(
                    **test_fields,
                )
            test_fields[field_name] = field_value

        post_comment = PostComment.objects.create(
            **test_fields
        )

        assert post_comment == PostComment.objects.last()

    def test_delete_generates_deleted_at(self):
        comment_info = (
            ('author', self.user),
            ('post', self.post),
            ('content', 'comment'),
        )

        post_comment = PostComment.objects.create(
            **dict(comment_info),
        )

        assert not post_comment.deleted_at
        post_comment.delete()
        assert post_comment.deleted_at

    def test_post_comment_reply(self):
        comment_info = (
            ('author', self.user),
            ('post', self.post),
            ('content', 'comment'),
        )

        post_comment = PostComment.objects.create(
            **dict(comment_info),
        )

        post_reply = PostComment.objects.create(
            **dict(comment_info),
            parent=post_comment,
        )

        assert post_comment.postcomment_set.last() == post_reply
