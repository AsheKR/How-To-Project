import pytest
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

    def test_list_create_post_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token']
        }

        context = {
            'category': 'category1',
            'title': 'title1',
            'content': 'content',
        }

        response = client.post(
            resolve_url('posts:list_create'),
            **header,
            data=context,
        )

        assert response.status_code == 201

        response = client.get(
            resolve_url('posts:list_create'),
        )

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_retrieve_update_destroy_post_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token']
        }

        context = {
            'category': 'category1',
            'title': 'title1',
            'content': 'content',
        }

        _ = client.post(
            resolve_url('posts:list_create'),
            **header,
            data=context,
        )

        context = {
            'category': 'category2',
            'title': 'title2',
            'content': 'content2',
        }

        response = client.get(
            resolve_url('posts:retrieve_update_destroy', pk=1),
        )

        assert response.status_code == 200

        response = client.patch(
            resolve_url('posts:retrieve_update_destroy', pk=1),
            **header,
            data=context,
            content_type='application/json'
        )

        assert response.json()['title'] == 'title2'
        assert response.json()['content'] == 'content2'

        response = client.delete(
            resolve_url('posts:retrieve_update_destroy', pk=1),
        )

        assert response.status_code == 204
