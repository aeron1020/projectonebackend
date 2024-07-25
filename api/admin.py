from django.contrib import admin
from django.utils.text import slugify
from .models import Post, Category, Comment, Like, Project


@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',),}

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Project)


