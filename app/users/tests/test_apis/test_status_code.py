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

    def test_create_user_user_id_start_with_numbers_occur_400(self, client):
        context = {
            'user_id': '1asdf11',
            'password': 'asd',
            'email': 'asd@asd.com',
            'nickname': 'asd',
        }

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_id_at_least_5_characters_long(self, client):
        context = {
            'user_id': 'asd',
            'password': 'asd',
            'email': 'asd@asd.com',
            'nickname': 'asd',
        }

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2051'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_id_maximum_15_characters_long(self, client):
        context = {
            'user_id': 'a234567890123456',
            'password': 'asd',
            'email': 'asd@asd.com',
            'nickname': 'asd',
        }

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2041'
        assert json['errors'][0]['field'] == 'user_id'
