from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
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
    )

    def like_toggle(self, user):
        obj, created = self.like_users.get_or_create(pk=user.pk)

        if not created:
            if obj.deleted_at:
                obj.deleted_at = None
                obj.save()
            else:
                obj.deleted_at = now()
                obj.save()
                return status.HTTP_204_NO_CONTENT

        return status.HTTP_201_CREATED
