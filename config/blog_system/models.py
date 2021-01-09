from django.db import models

from django.conf import settings
from taggit.managers import TaggableManager


class Post(models.Model):
    """
    Моедель поста пользователя
    """
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Owner',
    )
    title_image = models.ImageField(
        upload_to=f'blog/title_image/',
        verbose_name='title_image',
        blank=True
        # default='../static/img/account/noimage.png'
    )
    title = models.CharField(
        max_length=64,
        db_index=True,
        verbose_name='Title',
        blank=False
    )
    text = models.TextField(
        verbose_name='Text',
        blank=False
    )
    # TODO tags add
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Last update'
    )

    tags = TaggableManager()

    def __str__(self):
        return self.title