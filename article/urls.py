from django.urls import path
from .views import (
    article, 
    articleCreate, 
    articleRead, 
    articleUpdate, 
    articleDelete, 
    articleSearch,
    articleLike,
    commentCreate,
    commentUpdate,
    commentDelete,
)

app_name = 'article'
urlpatterns = [
    path('', article, name='article'),
    path('articleCreate/', articleCreate, name='articleCreate'),
    path('articleRead/<int:articleId>/', articleRead, name='articleRead'),
    path('articleUpdate/<int:articleId>/', articleUpdate, name='articleUpdate'),
    path('articleDelete/<int:articleId>', articleDelete, name='articleDelete'),
    path('articleSearch/', articleSearch, name='articleSearch'),
    path('articleLike/<int:articleId>', articleLike, name='articleLike'),
    path('commentCreate/<int:articleId>', commentCreate, name='commentCreate'),
    path('commentUpdate/<int:commentId>', commentUpdate, name='commentUpdate'),
    path('commentDelete/<int:commentId>', commentDelete, name='commentDelete'),
]