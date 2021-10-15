from django.contrib import admin
from .models import Post, Categories, PostComment



admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Categories)
