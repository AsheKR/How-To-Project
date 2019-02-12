from django.shortcuts import resolve_url


class BaseTestMixin:

    @staticmethod
    def _create_users(client, dump):
        context = {
            'user_id': dump,
            'password': 'asd',
            'email': dump + '@' + dump + '.com',
            'nickname': dump,
        }

        response = client.post(resolve_url('users:create'),
                               data=context)
        return response

    @staticmethod
    def _create_follow(client, header, user_id):
        response = client.post(
            resolve_url('users:following', user_id=user_id),
            **header,
        )

        return response
