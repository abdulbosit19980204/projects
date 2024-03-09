from django.contrib import admin
from .models import Article, Category, Comments, Tag, Contact


# Register your models here.
class CategoryInline(admin.TabularInline):
    model = Article
    extra = 0


class ArticleInline(admin.TabularInline):
    model = Comments
    extra = 0


class TagInline(admin.TabularInline):
    model = Article
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    list_display_links = ('id', "name")
    inlines = (CategoryInline,)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "updated_at", "is_published", "view_count")
    list_display_links = ('id', 'title')
    inlines = (ArticleInline,)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'article', "created_at", "is_visiable")
    list_display_links = ("id", 'name', 'article')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("id", "name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_responded', 'created_at')
    list_display_links = ('id', 'name', 'email')
