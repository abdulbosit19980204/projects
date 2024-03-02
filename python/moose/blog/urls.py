from django.urls import path

from .views import home_view, about_view, contact_view, blog_view, blog_info, subscribes, error_view

urlpatterns = [
    path('', home_view),
    path('blog/', blog_view),
    path('about/', about_view),
    path('contact', contact_view),
    path('blog/<int:pk>', blog_info),
    path('subscribes/', subscribes),
    path('404/', error_view),
]
