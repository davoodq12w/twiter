from django.contrib import admin
from .models import Post, Comment, Image

# Register your models here.


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'auther', 'publish', 'status']
    ordering = ['title']
    list_filter = ['publish', 'status']
    search_fields = ['title', 'description']
    raw_id_fields = ['auther']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']
    inlines = [ImageInline, CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['auther', 'post', 'create', 'status']
    ordering = ['create']
    list_filter = ['post', 'status']
    search_fields = ['text', 'auther']
    raw_id_fields = ['post']
    date_hierarchy = 'create'
    list_editable = ['status']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'create']
