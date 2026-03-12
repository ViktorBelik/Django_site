from django.db.models.base import Model
from django.shortcuts import render
from django.utils.safestring import SafeText
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls  import reverse, reverse_lazy
from .models import Article


class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")
    )


class ArticleDetailView(DetailView):
    model = Article


class LatestArticleFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Обновление при создании новых статей'
    link = reverse_lazy('blogapp:articles')
    
    def items(self):
        return (
            Article.objects
            .filter(published_at__isnull=False)
            .order_by("-published_at")[:5]
        )
    
    def item_title(self, item: Article):
        return item.title
    
    def item_description(self, item: Article) -> str:
        return item.body[:200]
    
    def item_link(self, item: Article) -> str:
        return reverse('blogapp:article', kwargs={"pk": item.pk})
    