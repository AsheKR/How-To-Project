from base.base_test_mixins import BaseTestMixin


class TestUserStatusCodeAPI(BaseTestMixin):

    def test_create_user_require_fields_occur_400(self, client):
        context = {
            'password': 'password',
            'email': 'email@email.com',
            'nickname': 'nickname'
        }

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
