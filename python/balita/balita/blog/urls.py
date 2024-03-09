from django.urls import path

from .views import home_view, about_view, categories_view, contact_view, article_info, tag_view, search_view

urlpatterns = [
    path('', home_view),
    path('about/', about_view),
    path('categories/', tag_view),
    path('categories/<int:pk>', categories_view),
    path('contact/', contact_view),
    path('category/<int:pk>', article_info),
    path('search/', search_view),
]
