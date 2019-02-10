from datetime import timedelta

import pytest
from django.shortcuts import resolve_url
from django.utils.timezone import now

from base.base_test_mixins import BaseTestMixin


class TestUserAPI(BaseTestMixin):

    def test_create_user_api(self, client):
        response = self._create_users(client, 'asd')

        assert response.status_code == 201, 'Create User API Status Code not 201'
        assert response.json()['token'], 'Create User API no Token Returned'

    def test_login_api(self, client):
        _ = self._create_users(client, 'asd')

        context = {
            'user_id': 'asd',
            'password': 'asd',
        }

        response = client.post(resolve_url('users:login'),
                               data=context)

        assert response.status_code == 200, 'Login Failed'
        assert response.json()['token'], 'Cannot Receive Token'

    def test_retrieve_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.get(
            resolve_url('users:profile', pk=1, ),
            **header,
        )

        assert response.status_code == 200, 'User Retrieve Failed'
        assert not response.json().get('password'), "Don't bring the password."
        assert not response.json().get('password'), "Don't bring deleted_at."

    def test_me_retrieve_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.get(
            resolve_url('users:me-profile', ),
            **header,
        )

        assert response.status_code == 200, 'User Retrieve Failed'

    def test_patch_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        context = {
            'nickname': '프와송',
            'description': '송와프',
        }

        response = client.patch(
            resolve_url('users:profile', pk=1, ),
            **header,
            data=context,
            content_type="application/json"
        )

        assert response.status_code == 200, 'User Patch Failed'

    def test_destroy_api(self, client, django_user_model):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.delete(
            resolve_url('users:profile', pk=1, ),
            **header,
            content_type="application/json"
        )

        assert response.status_code == 204, 'User Delete Failed'
        assert django_user_model.objects.get(pk=1).deleted_at, 'User Not Deleted'


class TestUserAPIValidation(BaseTestMixin):

    def test_anonymous_retrieve_me(self, client):
        response = client.get(
            resolve_url('users:me-profile', ),
        )

        assert response.status_code == 404

    @pytest.mark.smoke
    def test_cannot_retrieve_deleted_user(self, client, django_user_model):
        response = self._create_users(client, 'asd')
        django_user_model.objects.first().delete()

        response = client.get(
            resolve_url('users:profile', pk=1, ),
        )

        assert response.status_code == 404

    def test_patch_me_read_only_fields_error(self, client, django_user_model):
        response = self._create_users(client, 'asd')

        item_time = now() - timedelta(days=3)

        items = (
            ('created_at', item_time),
            ('deleted_at', item_time),
            ('password', 'qwe'),
        )

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        origin_user = django_user_model.objects.first()

        for field_name, field_value in items:
            response = client.patch(
                resolve_url('users:profile', pk=1, ),
                **header,
                data={field_name: field_value},
                content_type="application/json"
            )

            assert getattr(origin_user, field_name) == getattr(django_user_model.objects.first(), field_name)
