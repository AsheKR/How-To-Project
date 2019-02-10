from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token

from base.base_models import BaseIsDeletedModel
from users.managers import UserManager


class User(AbstractBaseUser, BaseIsDeletedModel, PermissionsMixin):
    user_id = models.CharField('유저아이디', max_length=15, unique=True, )
    email = models.EmailField('유저이메일', unique=True, )
    nickname = models.CharField('별명', max_length=15, )

    description = models.TextField('자기소개', blank=True, null=True)
    profile_image = models.ImageField('프로필 이미지', upload_to='profile/', blank=True, null=True)

    relation_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='UserRelation',
    )

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = ('유저', )
        verbose_name_plural = ('유저', )

    def delete(self, using=None, keep_parents=False):
        super().delete()
        Token.objects.filter(user=self).delete()


class UserRelation(BaseIsDeletedModel):

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_user_relation',
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_user_relation',
    )

    class Meta:
        unique_together = (
            ('to_user', 'from_user'),
        )
