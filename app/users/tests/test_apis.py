from django.shortcuts import resolve_url


class TestUserAPI:

    @staticmethod
    def _create_users(client, dump):
        context = {
            'user_id': dump,
            'password': 'asd',
            'email': dump+'@'+dump+'.com',
            'nickname': dump,
        }

        response = client.post(resolve_url('users:create'),
                               data=context)
        return response

    def test_create_user_api(self, client):
        response = self._create_users(client, 'asd')

        assert response.status_code == 201, 'Create User API Status Code not 201'
        assert response.json()['token'], 'Create User API no Token Returned'

    def test_login_api(self, client):
        _ = self._create_users(client, 'asd')

        context = {
            'user_id': 'asd',
            'password': 'asd',
        }

        response = client.post(resolve_url('users:login'),
                               data=context)

        assert response.status_code == 200, 'Login Failed'
        assert response.json()['token'], 'Cannot Receive Token'

    def test_retrieve_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.get(
            resolve_url('users:profile', pk=1, ),
            **header,
        )

        assert response.status_code == 200, 'User Retrieve Failed'
        assert not response.json().get('password'), "Don't bring the password."

    def test_me_retrieve_api(self, client):
        response = self._create_users(client, 'asd')

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + response.json()['token'],
        }

        response = client.get(
            resolve_url('users:me-profile', ),
            **header,
        )

        assert response.status_code == 200, 'User Retrieve Failed'
