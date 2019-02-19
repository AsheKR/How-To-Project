from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from rest_framework import status

from base.base_models import BaseIsDeletedModel


class PostCategory(models.Model):
    name = models.CharField(max_length=15, unique=True)


class Post(BaseIsDeletedModel):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        PostCategory,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100,
    )
    content = models.TextField()
    like_users = models.ManyToManyField(
        get_user_model(),
        symmetrical=False,
        blank=True,
        related_name='like_users',
        related_query_name='like_user',
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()

    def like_toggle(self, user):
        if self.like_users.filter(pk=user.pk).exists():
            self.like_users.remove(user)
            return status.HTTP_204_NO_CONTENT
        else:
            self.like_users.add(user)
            return status.HTTP_201_CREATED


class PostComment(BaseIsDeletedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        max_length=100,
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save()
