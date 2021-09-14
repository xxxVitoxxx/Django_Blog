from django.contrib import admin
from .models import Article, Comment
# Register your models here.

# 客製化Comment model
class CommentAdmin(admin.ModelAdmin):
    # 客製化頁面顯示清單:顯示article, content欄位
    list_display = ['article', 'content', 'pubDateTime']

    # 設定資料連結欄位，透過article連結
    list_display_links = ['article']

    # 設定過濾器：設定右方過濾欄位為article, content，點選即可濾出該項目的相關資料
    list_filter = ['article', 'content']

    # 設定搜尋欄位為content，輸入資料即可搜尋該欄位資料
    search_fields = ['content']

    # 設定content欄位可直接編輯
    list_editable = ['content']
    class Meta:
        model = Comment

# 在網頁admin顯示資料模型
admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)