from base.base_test_mixins import BaseTestMixin


class BaseTestUserContext:

    @staticmethod
    def _get_context(user_id='asd123', password='P@ssw04d',
                     email='test@test.com', nickname='지존짱짱맨'):
        return {
            'user_id': user_id,
            'password': password,
            'email': email,
            'nickname': nickname,
        }


class TestUserStatusCodeAPI(BaseTestMixin, BaseTestUserContext):

    def test_create_user_require_fields_occur_400(self, client):
        context = self._get_context('', '', '', '')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        for i, key in enumerate(tuple(context)):
            assert json['errors'][i]['code'] == '2031'
            assert json['errors'][i]['field'] == key

    def test_create_user_user_id_start_with_numbers_occur_400(self, client):
        context = self._get_context('1asdf11')
        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_id_at_least_5_characters_long(self, client):
        context = self._get_context('four')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2051'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_id_maximum_15_characters_long(self, client):
        context = self._get_context('a234567890123456')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2041'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_id_not_allow_uppercase(self, client):
        context = self._get_context('A0lowercase')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_id_not_allow_special_character_except_hypen_and_underline(self, client):
        context = self._get_context('[d(-_-)b]')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_password_at_least_8_characters_long(self, client):
        context = self._get_context(password='P@ssw0r')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2051'
        assert json['errors'][0]['field'] == 'password'

    def test_create_user_password_must_contain_at_least_1_digit(self, client):
        context = self._get_context(password='P@ssword')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'password'

    def test_create_user_password_must_contain_at_least_1_uppercase(self, client):
        context = self._get_context(password='p@ssword')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'password'

    def test_create_user_password_must_contain_at_least_1_character(self, client):
        context = self._get_context(password='Password')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'password'

