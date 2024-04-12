from django.urls import path

from .views import (home_view, profile_view, post_upload_view, post_comment_view,
                    post_like_view, following_view, profile_image_view, searched_view, post_delete_view,
                    post_comment_disabled_view, notification_read_view, notification_mark_read_view,
                    follower_view, following_view, add_favorite_view)

urlpatterns = [
    path('', home_view),
    path('profile/', profile_view),
    path('post/upload/', post_upload_view),
    path('post/comment/', post_comment_view),
    path('post/like/', post_like_view),
    path('post/delete/', post_delete_view),
    path('post/comment-disabled', post_comment_disabled_view),
    path('user/follow/', following_view),
    path('profile/image/', profile_image_view),
    path('searched/', searched_view),
    path('notification/', notification_read_view),
    path('notification/mark_read', notification_mark_read_view),
    path('follower/', follower_view),
    path('following/', following_view),
    path('favorite/', add_favorite_view),
]
