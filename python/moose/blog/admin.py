from django.contrib import admin

from .models import Articles, ContactUs, Comments, Subscribers, Category


# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullName', 'is_responsed', 'created_at')
    list_display_links = ('id', 'fullName', 'is_responsed')


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'main_page', 'created_at', 'updated_at')
    list_display_links = ('id', 'title', 'creator')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentor_name', 'commentor_email', 'is_Visable', 'article_id')
    list_display_links = ('id', 'commentor_name', 'commentor_email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(ContactUs, ContactAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Subscribers)
admin.site.register(Category, CategoryAdmin)
