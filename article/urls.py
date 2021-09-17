from django.urls import path
from .views import article, articleCreate, articleRead, articleUpdate

app_name = 'article'
urlpatterns = [
    path('', article, name='article'),
    path('articleCreate/', articleCreate, name='articleCreate'),
    path('articleRead/<int:articleId>', articleRead, name='articleRead'),
    path('articleUpdate/<int:articleId>', articleUpdate, name='articleUpdate'),
]