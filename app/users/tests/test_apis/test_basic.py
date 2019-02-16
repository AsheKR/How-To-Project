import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.test.client import encode_multipart

from base.base_test_mixins import BaseTestMixin
from users.models import UserRelation


class TestUserBasicAPI(BaseTestMixin):

    def teardown_method(self, client):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    def _test_create_user_api(self, client, user_id='user_id', email='email@email.com'):
        context = {
            'user_id': user_id,
            'password': 'P@ssw0rd',
            'email': email,
            'nickname': 'nickname'
        }

        response = self._create_users_with_context(client, context)

        assert response.status_code == 201

        user = get_user_model().objects.last()

        assert user.user_id == context['user_id']
        assert user.password
        assert user.email == context['email']
        return user, response

    def test_create_user_api_required_fields(self, client):
        _, response = self._test_create_user_api(client)

        assert response.json()['token']

    def test_patch_user_api_fill_all_fields(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        context = {
            'nickname': 'first',
            'description': 'first',
            'profile_image': self._create_image(),
        }

        enc_content = encode_multipart('BoUnDaRyStRiNg', context)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = client.patch(resolve_url('users:me-profile'),
                                **header,
                                data=enc_content,
                                content_type=content_type)

        assert response.status_code == 200

        user = get_user_model().objects.get(pk=1)

        json = response.json()

        assert json.get('user_id') == 'user_id'
        assert json.get('email') == 'email@email.com'
        assert json.get('created_at')
        assert json.get('description') == context['description']
        assert json.get('nickname') == context['nickname']

        assert user.profile_image.url in json.get('profile_image')
        assert os.path.exists(os.path.join(settings.MEDIA_ROOT, user.profile_image.path))

    def test_delete_user_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.delete(resolve_url('users:me-profile'),
                                 **header,)

        assert response.status_code == 204

        user = get_user_model().objects.get(pk=1)

        assert user.deleted_at

    def test_retrieve_user_api_named_profile(self, client):
        _, response = self._test_create_user_api(client)

        response = client.get(resolve_url('users:profile', user_id='user_id'))

        assert response.status_code == 200

        json = response.json()

        assert json.get('user_id') == 'user_id'
        assert json.get('email') == 'email@email.com'
        assert json.get('created_at')
        assert json.get('description') is None
        assert json.get('nickname') == 'nickname'

        assert json.get('profile_image') is None

    def test_retrieve_user_api_named_me_profile(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.get(resolve_url('users:me-profile'),
                              **header)

        assert response.status_code == 200

        json = response.json()

        assert json.get('user_id') == 'user_id'
        assert json.get('email') == 'email@email.com'
        assert json.get('created_at')
        assert json.get('description') is None
        assert json.get('nickname') == 'nickname'

        assert json.get('profile_image') is None

    def test_login_user_api(self, client):
        _, response = self._test_create_user_api(client)

        context = {
            'user_id': 'user_id',
            'password': 'P@ssw0rd',
        }

        response = client.post(resolve_url('users:login'),
                               data=context, )

        assert response.status_code == 200
        assert response.json()['token']

    def test_following_user_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')

        assert response.status_code == 201
        assert UserRelation.objects.filter(from_user__user_id='user_id', to_user__user_id='target').exists()

    def test_un_follow_user_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')
        response = self._create_follow(client, header, 'target')

        assert response.status_code == 204
        assert not UserRelation.objects.filter(from_user__user_id='user_id',
                                               to_user__user_id='target',
                                               deleted_at=None).exists()

    def test_re_follow_user_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')
        response = self._create_follow(client, header, 'target')

        assert response.status_code == 204
        assert not UserRelation.objects.filter(from_user__user_id='user_id',
                                               to_user__user_id='target',
                                               deleted_at=None).exists()

        response = self._create_follow(client, header, 'target')

        assert response.status_code == 201
        assert UserRelation.objects.filter(from_user__user_id='user_id',
                                           to_user__user_id='target',
                                           deleted_at=None).exists()

    def test_get_following_list_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')

        assert response.status_code == 201

        response = client.get(resolve_url('users:following', user_id='target'))

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_following_me_list_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _, target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')

        assert response.status_code == 201

        response = client.get(resolve_url('users:me-following'), **header)

        assert response.status_code == 200
        assert len(response.json()) == 0

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + target.json()['token'],
        }

        response = client.get(resolve_url('users:me-following'), **header)

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_follower_list_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')

        assert response.status_code == 201

        response = client.get(resolve_url('users:follower', user_id='user_id'))

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_follower_me_list_api(self, client):
        _, response = self._test_create_user_api(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _, target = self._test_create_user_api(client, user_id='target', email='ea@ea.com')

        response = self._create_follow(client, header, 'target')

        assert response.status_code == 201

        response = client.get(resolve_url('users:me-follower'), **header)

        assert response.status_code == 200
        assert len(response.json()) == 1

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + target.json()['token'],
        }

        response = client.get(resolve_url('users:me-follower'), **header)

        assert response.status_code == 200
        assert len(response.json()) == 0
