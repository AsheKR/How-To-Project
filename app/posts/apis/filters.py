import django_filters
from django.db.models import Q

from posts.models import Post


class PostFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='get_category', label='category')
    author = django_filters.CharFilter(method='get_author', label='author')
    search = django_filters.CharFilter(method='get_search', label='search')

    class Meta:
        model = Post
        fields = {
            'category': ['exact', ],
            'search': ['exact', ],
            'author': ['exact', ],
        }

    def get_author(self, qs, name, value):
        return qs.filter(
            author__user_id=value,
        )

    def get_category(self, qs, name, value):
        return qs.filter(
            category__name=value,
        )

    def get_search(self, qs, name, value):
        return qs.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )
