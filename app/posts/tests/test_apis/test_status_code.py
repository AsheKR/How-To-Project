from django.shortcuts import resolve_url

from base.base_test_mixins import BaseTestMixin


class TestRequiredFieldPostStatusCodeAPI(BaseTestMixin):

    def setup_method(self, method):
        self._create_post_category()

    def test_create_post_require_fields_occur_400(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = self._create_post(client, header, '', '', '')

        json = response.json()

        assert response.status_code == 400
        for i in range(len(json['errors'])):
            assert json['errors'][i]['code'] in ['2031', '2027']
            assert json['errors'][i]['message'] in ['이 필드는 blank일 수 없습니다.', '이 필드는 null일 수 없습니다.']


class TestValidateFieldPostStatusCodeAPI(BaseTestMixin):

    def setup_method(self, method):
        self._create_post_category()

    def test_create_post_category_not_exists_occur_400(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = self._create_post(client, header, category='3')

        json = response.json()

        assert response.status_code == 400
        assert json['errors'][0]['code'] == '2151'
        assert json['errors'][0]['field'] == 'category'
        assert '객체가 존재하지 않습니다.' in json['errors'][0]['message']

    def test_create_post_anonymous_user_occur_401(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {

        }

        response = self._create_post(client, header)

        json = response.json()

        assert response.status_code == 401

