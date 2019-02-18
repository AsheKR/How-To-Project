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

    def test_patch_post_require_fields_occur_400(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header)

        context = {
            'content': '',
            'title': '',
            'category': ''
        }

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=1),
                                **header,
                                data=context,
                                content_type='application/json')

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

    def test_retrieve_post_not_exists_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.get(resolve_url('posts:retrieve_update_destroy', pk=2))

        assert response.status_code == 404

    def test_retrieve_deleted_post_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                                 **header)

        assert response.status_code == 204

        response = client.get(resolve_url('posts:retrieve_update_destroy', pk=1))

        assert response.status_code == 404

    def test_patch_post_category_not_exists_occur_400(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header)

        context = {
            'content': 'changed',
            'title': 'change title',
            'category': '3'
        }

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=1),
                                **header,
                                data=context,
                                content_type='application/json')

        json = response.json()

        assert response.status_code == 400
        assert json['errors'][0]['code'] == '2151'
        assert json['errors'][0]['field'] == 'category'
        assert '객체가 존재하지 않습니다.' in json['errors'][0]['message']

    def test_patch_post_anonymous_user_occur_401(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        context = {
            'content': 'changed',
            'title': 'change title',
            'category': '2'
        }

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=1),
                                data=context,
                                content_type='application/json')

        assert response.status_code == 401

    def test_patch_post_not_exists_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        context = {
            'content': 'changed',
            'title': 'change title',
            'category': '2'
        }

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=3),
                                **header,
                                data=context,
                                content_type='application/json')

        assert response.status_code == 404

    def test_patch_post_deleted_post_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        context = {
            'content': 'changed',
            'title': 'change title',
            'category': '2'
        }

        _ = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                          **header)

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=1),
                                **header,
                                data=context,
                                content_type='application/json')

        assert response.status_code == 404

    def test_patch_post_must_owner(self, client):
        context = self._get_user_context()
        author_response = self._create_users_with_context(client, context)

        author = {
            'HTTP_AUTHORIZATION': 'Token ' + author_response.json()['token'],
        }

        _ = self._create_post(client, author, category='1')

        context = self._get_user_context(user_id='another_user', email='ano@ther.com')
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        context = {
            'content': 'changed',
            'title': 'change title',
            'category': '2'
        }

        response = client.patch(resolve_url('posts:retrieve_update_destroy', pk=1),
                                **header,
                                data=context,
                                content_type='application/json')

        assert response.status_code == 403

    def test_delete_post_anonymous_user_occur_401(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1))

        assert response.status_code == 401

    def test_delete_post_not_exists_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.delete(resolve_url('posts:retrieve_update_destroy', pk=3),
                                 **header)

        assert response.status_code == 404

    def test_delete_post_deleted_post_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        _ = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                          **header)

        response = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                                 **header)

        assert response.status_code == 404

