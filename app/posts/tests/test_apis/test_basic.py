from django.shortcuts import resolve_url

from base.base_test_mixins import BaseTestMixin


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
