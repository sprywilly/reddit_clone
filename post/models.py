from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    name = models.CharField(max_length=250)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Статья'
        verbose_name_plural='Статьи'

    def __str__(self):
        return "{0}".format(self.name)