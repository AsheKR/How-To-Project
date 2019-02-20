from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework.authtoken.models import Token

from base.base_test_mixins import BaseTestMixin
from posts.models import Post, PostCategory


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

    def test_like_post_anonymous_user_occur_401(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.post(resolve_url('posts:like', pk=1))

        assert response.status_code == 401

    def test_like_post_not_exists_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.post(resolve_url('posts:like', pk=2),
                               **header)

        assert response.status_code == 404

    def test_like_post_deleted_post_occur_404(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')
        _ = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                          **header)

        context = self._get_user_context(user_id='another_user', email='email@e.com')
        another_response = self._create_users_with_context(client, context)

        another_header = {
            'HTTP_AUTHORIZATION': 'Token ' + another_response.json()['token'],
        }

        response = client.post(resolve_url('posts:like', pk=1),
                               **another_header)

        assert response.status_code == 404

    def test_like_post_cannot_like_author_self_post(self, client):
        context = self._get_user_context()
        response = self._create_users_with_context(client, context)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        _ = self._create_post(client, header, category='1')

        response = client.post(resolve_url('posts:like', pk=1),
                               **header)

        assert response.status_code == 403

        json = response.json()

        assert json['code'] == '1101'
        assert json['message'] == '자신의 포스트에는 좋아요를 누를 수 없습니다.'
        assert json['field'] == 'like'


class TestRequireFieldPostCommentStatusCodeAPI(BaseTestMixin):

    def setup_method(self, method):
        user = get_user_model().objects.create_user(
            user_id='test123',
            password='P@ssw0rd',
            email='email@email.com',
        )
        self.header = {
            'HTTP_AUTHORIZATION': 'Token ' + Token.objects.get_or_create(user=user)[0].key
        }

        category = PostCategory.objects.create(name='category1')

        Post.objects.create(
            author=user,
            category=category,
            title='title1',
            content='content',
        )

    def test_create_post_comment_require_fields_occur_400(self, client):
        context = {
            'content': ''
        }
        response = client.post(resolve_url('posts:comment', pk=1),
                               data=context,
                               **self.header,)

        assert response.status_code == 400

        json = response.json()

        assert json['errors'][0]['code'] == '2031'
        assert json['errors'][0]['message'] == '이 필드는 blank일 수 없습니다.'
        assert json['errors'][0]['field'] == 'content'

    def test_patch_post_comment_require_fields_occur_400(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': ''
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=1),
                                **self.header,
                                data=context,
                                content_type='application/json')

        assert response.status_code == 400

        json = response.json()

        assert json['errors'][0]['code'] == '2031'
        assert json['errors'][0]['message'] == '이 필드는 blank일 수 없습니다.'
        assert json['errors'][0]['field'] == 'content'


class TestValidationFieldPostCommentStatusCodeAPI(BaseTestMixin):

    def setup_method(self, method):
        user = get_user_model().objects.create_user(
            user_id='test123',
            password='P@ssw0rd',
            email='email@email.com',
        )
        self.header = {
            'HTTP_AUTHORIZATION': 'Token ' + Token.objects.get_or_create(user=user)[0].key
        }

        category = PostCategory.objects.create(name='category1')

        Post.objects.create(
            author=user,
            category=category,
            title='title1',
            content='content',
        )

    def test_create_post_comment_anonymous_user_occur_401(self, client):
        context = {
            'content': 'Comment is here'
        }
        response = client.post(resolve_url('posts:comment', pk=1),
                               data=context)

        assert response.status_code == 401

    def test_create_post_comment_not_exists_occur_404(self, client):
        context = {
            'content': 'Comment is here'
        }
        response = client.post(resolve_url('posts:comment', pk=2),
                               data=context,
                               **self.header,)

        assert response.status_code == 404

    def test_create_post_comment_deleted_post_occur_404(self, client):
        context = {
            'content': 'Comment is here'
        }

        _ = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                          **self.header)

        response = client.post(resolve_url('posts:comment', pk=1),
                               data=context,
                               **self.header,)

        assert response.status_code == 404

    def test_patch_post_comment_anonymous_user_occur_401(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=1),
                                data=context,
                                content_type='application/json')

        assert response.status_code == 401

    def test_patch_post_comment_not_exists_post_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=2,
                                            pk=1),
                                data=context,
                                content_type='application/json')

        assert response.status_code == 404

    def test_patch_post_comment_not_exists_post_comment_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=2),
                                data=context,
                                content_type='application/json')

        assert response.status_code == 404

    def test_patch_post_comment_deleted_post_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        _ = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                          **self.header,
                          data=context)

        context = {
            'content': 'Comment Changed'
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=1),
                                data=context,
                                **self.header,
                                content_type='application/json')

        assert response.status_code == 404

    def test_patch_post_comment_deleted_post_comment_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        _ = client.delete(resolve_url('posts:comment_update_delete',
                                      post_pk=1,
                                      pk=1),
                          **self.header,
                          data=context)

        context = {
            'content': 'Comment Changed'
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=1),
                                data=context,
                                **self.header,
                                content_type='application/json')

        assert response.status_code == 404

    def test_patch_post_comment_must_owner(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        another_user = get_user_model().objects.create_user(
            user_id='another123',
            password='P@ssw0rd',
            email='ano@ther.com',
        )

        another_header = {
            'HTTP_AUTHORIZATION': 'Token ' + Token.objects.get_or_create(user=another_user)[0].key
        }

        response = client.patch(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=1),
                                data=context,
                                **another_header,
                                content_type='application/json')

        assert response.status_code == 403

    def test_delete_post_comment_anonymous_user_occur_401(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        response = client.delete(resolve_url('posts:comment_update_delete',
                                             post_pk=1,
                                             pk=1))

        assert response.status_code == 401

    def test_delete_post_comment_not_exists_post_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        response = client.delete(resolve_url('posts:comment_update_delete',
                                             post_pk=2,
                                             pk=1),
                                 **self.header,
                                 data=context,
                                 content_type='application/json')

        assert response.status_code == 404

    def test_delete_post_comment_not_exists_post_comment_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        response = client.delete(resolve_url('posts:comment_update_delete',
                                             post_pk=1,
                                             pk=2),
                                 data=context,
                                 **self.header,
                                 content_type='application/json')

        assert response.status_code == 404

    def test_delete_post_comment_deleted_post_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        _ = client.delete(resolve_url('posts:retrieve_update_destroy', pk=1),
                          **self.header,
                          data=context)

        context = {
            'content': 'Comment Changed'
        }

        response = client.delete(resolve_url('posts:comment_update_delete',
                                            post_pk=1,
                                            pk=1),
                                data=context,
                                **self.header,
                                content_type='application/json')

        assert response.status_code == 404

    def test_delete_post_comment_deleted_post_comment_occur_404(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        _ = client.delete(resolve_url('posts:comment_update_delete',
                                      post_pk=1,
                                      pk=1),
                          **self.header,
                          data=context)

        context = {
            'content': 'Comment Changed'
        }

        response = client.delete(resolve_url('posts:comment_update_delete',
                                             post_pk=1,
                                             pk=1),
                                 data=context,
                                 **self.header,
                                 content_type='application/json')

        assert response.status_code == 404

    def test_delete_post_comment_must_owner(self, client):
        context = {
            'content': 'Comment is this'
        }
        _ = client.post(resolve_url('posts:comment', pk=1),
                        data=context,
                        **self.header, )

        context = {
            'content': 'Comment Changed'
        }

        another_user = get_user_model().objects.create_user(
            user_id='another123',
            password='P@ssw0rd',
            email='ano@ther.com',
        )

        another_header = {
            'HTTP_AUTHORIZATION': 'Token ' + Token.objects.get_or_create(user=another_user)[0].key
        }

        response = client.delete(resolve_url('posts:comment_update_delete',
                                             post_pk=1,
                                             pk=1),
                                 data=context,
                                 **another_header,
                                 content_type='application/json')

        assert response.status_code == 403

