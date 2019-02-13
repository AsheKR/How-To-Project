"""
필수 입력 값 / 모든 입력값 2개의 테스트 케이스로 테스트를 수행한다.
"""

from django.contrib.auth import get_user_model

from base.base_test_mixins import BaseTestMixin


class TestUserBasicAPI(BaseTestMixin):

    def _test_create_user_api(self, client, context):
        response = self._create_users_with_context(client, context)

        assert response.status_code == 201

        user = get_user_model().objects.get(pk=1)

        assert user.user_id == context['user_id']
        assert user.password
        assert user.email == context['email']
        return user

    def test_create_user_api_required_fields(self, client):
        context = {
            'user_id': 'user_id',
            'password': 'password',
            'email': 'email@email.com',
            'nickname': 'nickname'
        }

        self._test_create_user_api(client, context)
