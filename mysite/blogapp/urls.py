from django.urls import path
from .views import ArticlesListView, ArticleDetailView, LatestArticleFeed


app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticlesListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticleFeed(), name='articles-feed'),
]
