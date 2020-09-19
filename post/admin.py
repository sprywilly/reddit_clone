from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Post._meta.fields]
	list_filter = ('is_published', 'created', 'author')
	search_fields = ('name', 'text')
	ordering = ['created']

	class Meta:
		model = Post
			
		
admin.site.register(Post, PostAdmin)
