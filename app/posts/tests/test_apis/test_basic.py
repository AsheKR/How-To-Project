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
