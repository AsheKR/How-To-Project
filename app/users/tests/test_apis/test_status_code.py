from django.shortcuts import resolve_url
from django.test.client import encode_multipart

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

    @staticmethod
    def _get_patch_context(nickname='nickname', description='description', file=None):
        return {
            'nickname': nickname,
            'description': description,
            'file': file,
        }

    @staticmethod
    def _patch_user_with_context(client, header, context):
        enc_content = encode_multipart('BoUnDaRyStRiNg', context)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = client.patch(resolve_url('users:me-profile'),
                                **header,
                                data=enc_content,
                                content_type=content_type)

        return response


class TestRequiredFieldUserStatusCodeAPI(BaseTestMixin, BaseTestUserContext):

    def test_create_user_require_fields_occur_400(self, client):
        context = self._get_context('', '', '', '')

        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        for i, key in enumerate(tuple(context)):
            assert json['errors'][i]['code'] == '2031'
            assert json['errors'][i]['field'] == key

    def test_patch_user_require_fields_occur_400(self, client):
        context = self._get_context()

        response = self._create_users_with_context(client, context)

        context = self._get_patch_context('', '', '')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = self._patch_user_with_context(client, header, context)

        json = response.json()

        assert response.status_code == 400
        assert json['errors'][0]['code'] == '2031'
        assert json['errors'][0]['field'] == 'nickname'
        assert json['errors'][0]['message'] == '이 필드는 blank일 수 없습니다.'


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

    def test_retrieve_user_not_retrieve_non_user(self, client):
        response = client.get(resolve_url('users:profile', user_id='user_id'))

        assert response.status_code == 404

    def test_retrieve_user_not_retrieve_deleted_user(self, client):
        context = self._get_context(user_id='retrieve_me')

        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.get(resolve_url('users:profile', user_id='retrieve_me'))

        assert response.status_code == 200

        _ = client.delete(resolve_url('users:me-profile'),
                          **header, )

        response = client.get(resolve_url('users:profile', user_id='retrieve_me'))

        assert response.status_code == 404

    def test_not_retrieve_me_profile_by_anonymous_user(self, client):
        response = client.get(resolve_url('users:me-profile', ))

        assert response.status_code == 401

        response = client.patch(resolve_url('users:me-profile', ))

        assert response.status_code == 401

        response = client.delete(resolve_url('users:me-profile', ))

        assert response.status_code == 401


class TestUniqueConstraintUserStatusCodeAPI(BaseTestMixin, BaseTestUserContext):

    def test_create_user_user_id_must_unique(self, client):
        context = self._get_context()
        _ = self._create_users_with_context(client, context)

        context = self._get_context()
        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '3001'
        assert json['errors'][0]['field'] == 'user_id'

    def test_create_user_user_email_must_unique(self, client):
        context = self._get_context()
        _ = self._create_users_with_context(client, context)

        context = self._get_context(user_id='user_id')
        response = self._create_users_with_context(client, context)

        assert response.status_code == 400
        json = response.json()

        assert json['errors'][0]['code'] == '3001'
        assert json['errors'][0]['field'] == 'email'


class TestAnotherUserStatusCodeAPI(BaseTestMixin, BaseTestUserContext):

    def test_create_user_cannot_create_with_logged_in_status(self, client):
        context = self._get_context()

        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.post(resolve_url('users:create'),
                               **header)

        assert response.status_code == 403

        json = response.json()

        assert json['code'] == '1003'
        assert json['field'] == 'user_failed'
        assert json['message'] == '로그인된 유저로 실행할 수 없습니다.'

    def test_login_user_login_fail(self, client):
        context = self._get_context()

        _ = self._create_users_with_context(client, context)

        context = {
            'user_id': 'failedID',
            'password': 'P@ssw04d',
        }

        response = client.post(resolve_url('users:login'),
                               data=context, )

        assert response.status_code == 400

        json = response.json()

        assert json['code'] == '1002'
        assert json['field'] == 'user_failed'
        assert json['message'] == '아이디 혹은 비밀번호가 잘못되었습니다.'

    def test_login_user_cannot_get_token_with_logged_in_status(self, client):
        context = self._get_context()

        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        context = {
            'user_id': 'asd123',
            'password': 'P@ssw04d',
        }

        response = client.post(resolve_url('users:login'),
                               **header,
                               data=context, )

        assert response.status_code == 403

        json = response.json()

        assert json['code'] == '1003'
        assert json['field'] == 'user_failed'
        assert json['message'] == '로그인된 유저로 실행할 수 없습니다.'

    def test_login_user_cannot_get_deleted_user(self, client):
        context = self._get_context()

        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = client.delete(resolve_url('users:me-profile'),
                          **header,
                          data=context, )

        context = {
            'user_id': 'asd123',
            'password': 'P@ssw04d',
        }

        response = client.post(resolve_url('users:login'),
                               data=context, )

        assert response.status_code == 403

        json = response.json()

        assert json['code'] == '1004'
        assert json['field'] == 'user_failed'
        assert json['message'] == '삭제 진행중인 계정입니다.'
