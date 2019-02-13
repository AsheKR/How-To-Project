from base.base_test_mixins import BaseTestMixin


class TestUserStatusCodeAPI(BaseTestMixin):

    def test_create_user_require_fields_occur_400(self, client):
        context = {
            'user_id': '',
            'password': '',
            'email': '',
            'nickname': '',
        }

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        for i, key in enumerate(tuple(context)):
            assert json['errors'][i]['code'] == '2031'
            assert json['errors'][i]['field'] == key
