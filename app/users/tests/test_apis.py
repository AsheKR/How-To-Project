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

        response = client.post(resolve_url('users:user_create'),
                               data=context)
        return response

    def test_create_user_api(self, client):
        response = self._create_users(client, 'asd')

        assert response.status_code == 201, 'Create User API Status Code not 201'
        assert response.json()['token'], 'Create User API no Token Returned'
