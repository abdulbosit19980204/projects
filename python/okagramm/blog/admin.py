from django.contrib import admin
from .models import MyUser, FollowMyUser, Post, CommentPost, LikePost, Notification, FavoritePost
from django.utils.html import format_html


# Register your models here.

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.post_image.url))

    image_tag.short_description = 'Image'

    list_display = ('id', 'image_tag', 'author', 'like_count', 'write_comment', 'created_at',)
    list_display_links = ('id', 'author', 'like_count')


@admin.register(FollowMyUser)
class FollowMyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    list_display_links = ('id', 'follower', 'following', 'created_at')


@admin.register(CommentPost)
class CommentPostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(obj.post.post_image.url))

    image_tag.short_description = 'Image'
    list_display = ('id', 'image_tag', 'message', 'author', "created_at")
    list_display_links = ('id', 'image_tag', 'message', 'author',)


admin.site.register(LikePost)
admin.site.register(Notification)
admin.site.register(FavoritePost)
