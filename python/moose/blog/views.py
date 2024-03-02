from django.shortcuts import render, redirect

from .models import Articles, ContactUs, Comments, Subscribers
import requests
from django.core.paginator import Paginator

BOT_TOKEN = '6189703946:AAGb1TA2yDg-sdu0c_AIDn39_07AuzvlZgE'
CHAT_ID = '1209619850'


# Create your views here.

def home_view(request):
    articles = Articles.objects.filter(main_page=True, is_published="True").order_by('-view_count')[:3]
    d = {
        "articles": articles,
        "home": "active"
    }
    return render(request, 'index.html', context=d)


def blog_view(request):
    data = request.GET
    cat = data.get('cat', None)
    page = data.get('page', 1)
    if cat != None:
        articles = Articles.objects.filter(is_published=True, category=cat)
        d = {
            "articles": articles[::-1],
            "message": "Articles are loading...",
            "blog": "active",
        }
        return render(request, "blog.html", context=d)

    articles = Articles.objects.filter(is_published=True)
    page_obj = Paginator(articles, 3)

    d = {
        "message": "Articles are loading...",
        "blog": "active",
        "articles": page_obj.get_page(page)
    }

    return render(request, "blog.html", context=d)


def blog_info(request, pk):
    if request.method == "POST":
        comment = request.POST
        obj = Comments.objects.create(commentor_name=comment['name'], comment_message=comment['message'],
                                      commentor_email=comment['email'], commentor_telegram=comment['telegram'],
                                      article_id=pk)
        obj.save()
        return redirect(f'/blog/{pk}')
    article = Articles.objects.get(id=pk)
    article.view_count += 1
    article.save(update_fields=['view_count'])
    comments = Comments.objects.filter(article_id=pk, is_Visable=True)
    d = {
        'article': article,
        'comments': comments,
        'comment': len(comments),
        "blog": "active"
    }
    return render(request, 'blog-single.html', context=d)


def about_view(request):
    d = {"about": "active"}
    return render(request, 'about.html', context=d)


def contact_view(request):
    if request.method == "POST":
        data = request.POST
        obj = ContactUs.objects.create(fullName=data['name'], email=data['email'], subject=data['subject'],
                                       message=data['message'])
        obj.save()
        TEXT = f"""Yangi xabar qoldirildi:
        ID: {obj.id} 
        FIO: {obj.fullName} 
        Email: {obj.email}
        Subject: {obj.subject}
        Message: {obj.message}
        Time: {obj.created_at}
        """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={TEXT}'
        response = requests.get(url)
        print(response)
        return redirect(f'/contact')
    return render(request, 'contact.html', context={"contact": "active"})


def subscribes(request):
    if request.method == "POST":
        print("==" * 50)
        print(request)
        print('==' * 50)
    # subEmail = request.POST
    # obj = Subscribers.objects.create(subscriber_email=subEmail['email'])
    # obj.save()

    return render(request, 'index.html')


def error_view(request):
    return render(request, '404.html')
