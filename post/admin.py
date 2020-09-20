from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]
    list_filter = ('is_published', 'created', 'author')
    search_fields = ('name', 'text')
    ordering = ['created']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.fields]

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
