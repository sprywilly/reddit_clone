from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Post(models.Model):

    name = models.CharField('Назавние статьи', max_length=250)
    text = models.TextField('Текст статьи')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата обновления', auto_now=True)
    is_published = models.BooleanField('Опубликована', default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return "{0}".format(self.name)


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.CASCADE)

    user_comment = models.CharField('Комментарий', max_length=500)
    date_added = models.DateTimeField('Дата добавления', auto_now_add=True)

    approved = models.BooleanField('Подтвержден', default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['date_added']

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.user_comment[:20]
