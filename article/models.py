from django.db import models
from acc.models import User

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    content = models.TextField()
    pubDateTime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    class Meta:
        # 時間反向排序
        ordering = ['-pubDateTime']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # 當文章被刪除，該文章的留言也一並被刪除
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 當使用者被刪除，該使用者的留言通通一並被刪除
    content = models.CharField(max_length=128)
    pubDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.title + '-' + str(self.id)
    
    class Meta:
        # 時間正向排序
        ordering = ['pubDateTime']