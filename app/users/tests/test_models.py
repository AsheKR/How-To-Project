import pytest

from base.base_test_mixins import BaseTestMixin


class TestUserModel(BaseTestMixin):

    def test_required_fields(self, django_user_model):
        user_info = (
            ('user_id', 'asd'),
            ('password', 'asd'),
            ('email', 'asd@asd.com'),
        )
        test_fields = dict()

        for field_name, field_value in user_info:
            with pytest.raises(TypeError) as e:
                django_user_model.objects.create_user(
                    **test_fields,
                )
            test_fields[field_name] = field_value

        user = django_user_model.objects.create_user(
            **test_fields
        )

        assert user == django_user_model.objects.first()
