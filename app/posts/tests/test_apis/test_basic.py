from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

from base.base_test_mixins import BaseTestMixin
from posts.models import PostCategory, Post


class TestPostCategoryAPI(BaseTestMixin):

    def setup_method(self, method):
        self._create_post_category()

    def test_get_category_api(self, client):
        response = client.get(
            resolve_url('posts:category')
        )

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestPostAPI(BaseTestMixin):

    def setup_method(self, method):
        self._create_post_category()

    def test_create_post_api(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token']
        }

        context = {
            'category': '1',
            'title': 'title1',
            'content': 'content',
        }

        response = client.post(
            resolve_url('posts:list_create'),
            **header,
            data=context,
        )

        assert response.status_code == 201

    def test_get_post_list_api(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.get(resolve_url('posts:list_create'))

        assert response.status_code == 200

        json = response.json()

        assert len(json) == 1
        assert json[0]['id']
        assert json[0]['created_at']
        assert json[0]['modified_at']
        assert json[0]['title']
        assert json[0]['content']
        assert json[0]['author']
        assert json[0]['category']

    def test_get_post_api(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.get(resolve_url('posts:retrieve_update_destroy', pk=1))

        assert response.status_code == 200

        json = response.json()

        assert json['id']
        assert json['created_at']
        assert json['modified_at']
        assert json['title']
        assert json['content']
        assert json['author']
        assert json['category']

    def test_patch_post_api(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        context = {
            'content': 'changed',
            'title': 'change title',
            'category': '2'
        }

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=1),
                                **header,
                                data=context,
                                content_type='application/json')

        assert response.status_code == 200

        json = response.json()

        assert json['content'] == 'changed'
        assert json['title'] == 'change title'
        assert json['category'] == 2

    def test_delete_post_api(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                                 **header)

        assert response.status_code == 204

    def test_like_post_api(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        context = self._get_user_context(user_id='another_user', email='email@e.com')
        another_response = self._create_users_with_context(client, context)

        another_header = {
            'HTTP_AUTHORIZATION': 'Token ' + another_response.json()['token'],
        }

        response = client.post(resolve_url('posts:like', pk=1),
                               **another_header)

        assert response.status_code == 201


class TestPostCommentAPI(BaseTestMixin):

    def setup_method(self, client):
        self.user = get_user_model().objects.create_user(
            user_id='test123',
            password='P@ssw0rd',
            email='email@email.com',
        )
        self.category = PostCategory.objects.create(name='category1')

        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title='title1',
            content='content',
        )

    # def test_create_post_comment_api(self, client):
    #     context = {
    #         'user_id': 'test123',
    #         'password': 'P@ssw0rd',
    #     }
    #
    #     response = client.post(resolve_url('users:login'),
    #                            data=context, )
    #
    #     header = {
    #         'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
    #     }
    #
    #     context = {
    #         'content': 'comment',
    #     }
    #
    #     response = client.post(resolve_url('posts:comment', pk=1),
    #                            **header)
    #
    #     assert response.status_code == 201


class TestFilteringPostStatusCodeAPI(BaseTestMixin):

    def setup_method(self, method):
        self._create_post_category()

    def test_get_list_filter_category_name(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.get(resolve_url('posts:list_create')+'?category=category1')

        assert response.status_code == 200

        json = response.json()
        assert len(json) == 1

        response = client.get(resolve_url('posts:list_create') + '?category=category2')

        assert response.status_code == 200

        json = response.json()
        assert len(json) == 0

    def test_get_list_filter_author_name(self, client):
        context = self._get_user_context(user_id='filtername')
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.get(resolve_url('posts:list_create') + '?author=filtername')

        assert response.status_code == 200

        json = response.json()
        assert len(json) == 1

    def test_get_list_filter_search_content(self, client):
        context = self._get_user_context(user_id='filtername')
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.get(resolve_url('posts:list_create') + '?search=t')

        assert response.status_code == 200

        json = response.json()
        assert len(json) == 1
