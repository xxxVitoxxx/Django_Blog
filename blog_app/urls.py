from django.urls import path
from blog_app import views
from .views import main, about

app_name = 'blog_app'

# name是html檔在設奠連結時呼叫url的名稱
# href="{% url 'blog_app:main' %}"
urlpatterns = [
    path('', main, name='main'),
    path('about/', about, name='about'),
]