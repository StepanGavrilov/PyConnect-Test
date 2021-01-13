from django.db import models

from django.conf import settings


class Post(models.Model):
    """
    Моедель поста пользователя
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='posts',
        verbose_name='Owner',
    )
    title_image = models.ImageField(
        upload_to=f'blog/title_image/',
        verbose_name='title_image',
        blank=True,
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

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('created', )

    @property
    def image_url(self):
        if self.title_image and hasattr(self.title_image, 'url'):
            return self.title_image.url

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    """
    Комментарий под пост
    """
    post = models.ForeignKey(
        Post,
        db_index=True,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Post',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Author',
    )
    text = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Comment'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Last update'
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ('created', )