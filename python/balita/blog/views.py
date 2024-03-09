from django.shortcuts import render, redirect
from .models import Article, Category, Comments, Tag, Contact
from django.core.paginator import Paginator
from django.db.models import Q
from .search import search

categories = Category.objects.all()


# Create your views here.

def home_view(request):
    data = request.GET
    page = data.get('page', 1)

    categories = Category.objects.all()
    articles = Article.objects.all().order_by('category', '-created_at')
    page_obj = Paginator(articles, 4)
    popular = Article.objects.all().order_by('-view_count')
    vc = popular[(len(popular) // 2)].view_count
    more_blog_posts = Article.objects.filter(view_count__lte=vc).order_by('-created_at')
    popular_article = Article.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    d = {
        "home": "active",
        "categories": categories,
        "slider_article": articles[3:(len(articles) - 3)],
        "popular_article": popular_article[:3],
        "articles": page_obj.get_page(page),
        "more_blog_posts": more_blog_posts[:3],
        "popular": popular[:3],
        "tags": tags,
        "latests_footer": popular_article[:3]
    }
    return render(request, 'index.html', context=d)


def about_view(request):
    data = request.GET
    latest = Article.objects.all().order_by('-created_at')
    page = data.get('page', 1)
    page_article = Paginator(latest, 3)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular = Article.objects.all().order_by('-view_count')
    d = {
        "about": "active",
        "categories": categories,
        "popular": popular[:3],
        "tags": tags,
        "latest": page_article.get_page(page),
        "latests_footer": latest[:3]
    }
    return render(request, 'about.html', context=d)


def tag_view(request):
    data = request.GET
    tag = data.get('tag', None)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    popular = Article.objects.all().order_by('-view_count')
    cat_name = Tag.objects.filter(id=int(tag))
    latest = Article.objects.all().order_by('-created_at')
    if tag != None:
        articles = Article.objects.filter(tags=int(tag))
        d = {
            "articles": articles,
            "category": "active",
            "categories": categories,
            "cat_name": cat_name[0],
            "popular": popular[:3],
            "tags": tags,
            "latests_footer": latest[:3]
        }
        return render(request, 'category.html', context=d)


def categories_view(request, pk):
    data = request.GET
    articles = Article.objects.filter(category=pk)
    page = data.get('page', 1)
    page_obj = Paginator(articles, 6)
    categories = Category.objects.all()
    cat_name = Category.objects.filter(id=pk)
    tags = Tag.objects.all()
    popular = Article.objects.all().order_by('-view_count')
    latest = Article.objects.all().order_by('-created_at')
    d = {
        "articles": page_obj.get_page(page),
        "category": "active",
        "categories": categories,
        "cat_name": cat_name[0],
        "popular": popular[:3],
        "tags": tags,
        "latests_footer": latest[:3]
    }
    return render(request, 'category.html', context=d)


def article_info(request, pk):
    if request.method == "POST":
        comment = request.POST
        obj = Comments.objects.create(name=comment['name'], email=comment['email'], telegram=comment['telegram'],
                                      comment=comment['comment'], article_id=pk)
        obj.save()
        return redirect(f'/category/{pk}')

    detail = Article.objects.filter(id=pk).first()
    detail.view_count += 1
    comments = Comments.objects.filter(article_id=pk, is_visiable=True)
    detail.save(update_fields=['view_count'])
    popular = Article.objects.all().order_by('-view_count')
    tags = Tag.objects.all()
    reletad_tag = [i for i in detail.tags.all()]
    latest = Article.objects.all().order_by('-created_at')

    d = {
        "category": "active",
        "categories": categories,
        "comments": comments,
        "detail": detail,
        "len_comment": len(comments),
        "popular": popular[:3],
        "tags": tags,
        "latests_footer": latest[:3]
    }
    return render(request, 'blog-single.html', context=d)


def contact_view(request):
    if request.method == "POST":
        data = request.POST
        contact_data = Contact.objects.create(name=data['name'], phone=data['phone'], email=data['email'],
                                              message=data['message'])
        contact_data.save()
        return redirect('/contact')
    popular = Article.objects.all().order_by('-view_count')
    latest = Article.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    d = {
        "contact": "active",
        "categories": categories,
        "popular": popular[:3],
        "tags": tags,
        "latests_footer": latest[:3]
    }
    return render(request, 'contact.html', context=d)


def search_view(request):
    if request.method == "POST":
        data = request.POST
        query = data['key_word']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        articles = Article.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        articles = Article.objects.filter(is_published=True)

    page = request.GET.get('page', 1)
    page_obj = Paginator(articles, 6)
    tags = Tag.objects.all()
    popular = Article.objects.all().order_by('-view_count')
    latest = Article.objects.all().order_by('-created_at')

    d = {
        "articles": page_obj.get_page(page),
        "category": "active",
        "categories": Category.objects.all(),
        "popular": popular[:3],
        "cat_name": query,
        "tags": tags,
        "latests_footer": latest
    }
    return render(request, 'category.html', context=d)
