from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # 回傳所有參數
        #fields = '__all__'
        # 序列化要回傳的參數
        fields = ('id', 'title', 'content')