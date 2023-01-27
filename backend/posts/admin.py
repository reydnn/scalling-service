from django.contrib import admin

from posts.models import Comment, Post, PostTag


class PostTagInline(admin.TabularInline):
    model = PostTag
    fields = ["tag"]


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["content", "author", "created_at"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "content",
        "user",
        "likes",
    ]
    inlines = [PostTagInline, CommentInline]
