from .models import Article, Category, Comments, Tag

result_articles = []


def search(key):
    articles = Article.objects.all()
    if len(result_articles) != 0:
        result_articles.clear()

    for article in articles:
        if key in article.title:
            print('*==*' * 10)
            print(article)
            print('*==*' * 10)
            result_articles.append(article)
    return result_articles

# or key in article.description or key in article.tags or key in article.category
