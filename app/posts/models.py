from django.db import models


class PostCategory(models.Model):
    name = models.CharField(max_length=15, unique=True)
