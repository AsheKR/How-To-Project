from django.shortcuts import resolve_url

from base.base_test_mixins import BaseTestMixin


class TestPostCategoryAPI(BaseTestMixin):

    def test_get_category_api(self, client):
        self._create_post_category()
        response = client.get(
            resolve_url('posts:category')
        )

        assert response.status_code == 200
        assert len(response.json()) == 2
