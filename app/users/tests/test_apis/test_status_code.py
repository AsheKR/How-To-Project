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


class TestRequiredFieldUserStatusCodeAPI(BaseTestMixin, BaseTestUserContext):

    def test_create_user_require_fields_occur_400(self, client):
        context = self._get_context('', '', '', '')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        for i, key in enumerate(tuple(context)):
            assert json['errors'][i]['code'] == '2031'
            assert json['errors'][i]['field'] == key


class TestValidateFieldUserStatusCodeAPI(BaseTestMixin, BaseTestUserContext):

    def test_create_user_user_id_start_with_numbers_occur_400(self, client):
        context = self._get_context('1asdf11')
        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'
        assert '이 필드는 숫자로 시작하면 안됩니다.' in json['errors'][0]['message']

    def test_create_user_user_id_at_least_5_characters_long(self, client):
        context = self._get_context('four')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2051'
        assert json['errors'][0]['field'] == 'user_id'
        assert '이 필드의 글자 수가 5자 이상인지 확인하십시오.' in json['errors'][0]['message']

    def test_create_user_user_id_maximum_15_characters_long(self, client):
        context = self._get_context('a234567890123456')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2041'
        assert json['errors'][0]['field'] == 'user_id'
        assert '이 필드의 글자 수가 15 이하인지 확인하십시오.' in json['errors'][0]['message']

    def test_create_user_user_id_not_allow_uppercase(self, client):
        context = self._get_context('A0lowercase')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'
        assert '이 필드는 반드시 소문자로 작성되어야합니다.' in json['errors'][0]['message']

    def test_create_user_user_id_not_allow_special_character_except_hypen_and_underline(self, client):
        context = self._get_context('[d(-_-)b]')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'user_id'
        assert '유저 아이디에는 오직 "_"와 "-"만 허용합니다.' in json['errors'][0]['message']

    def test_create_user_password_at_least_8_characters_long(self, client):
        context = self._get_context(password='P@ssw0r')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2051'
        assert json['errors'][0]['field'] == 'password'
        assert '이 필드의 글자 수가 8자 이상인지 확인하십시오.' in json['errors'][0]['message']

    def test_create_user_password_must_contain_at_least_1_digit(self, client):
        context = self._get_context(password='P@ssword')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'password'
        assert '이 필드는 반드시 하나 이상의 숫자를 포함하여야 합니다' in json['errors'][0]['message']

    def test_create_user_password_must_contain_at_least_1_uppercase(self, client):
        context = self._get_context(password='p@ssw0rd')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'password'
        assert '이 필드는 반드시 A-Z까지의 대문자를 포함하여야 합니다.' in json['errors'][0]['message']

    def test_create_user_password_must_contain_at_least_1_character(self, client):
        context = self._get_context(password='Passw0rd')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '2013'
        assert json['errors'][0]['field'] == 'password'
        assert '이 필드는 반드시 특수문자가 하나 이상 포함되어야 합니다.' in json['errors'][0]['message']
