from django.urls import path
from .views import article, articleCreate, articleRead

app_name = 'article'
urlpatterns = [
    path('', article, name='article'),
    path('articleCreate/', articleCreate, name='articleCreate'),
    path('articleRead/<int:articleId>', articleRead, name='articleRead')
]