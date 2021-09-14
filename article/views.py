from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm
from django.contrib import messages
from django.http import Http404

# Create your views here.
def article(request):
    '''
    show article page
    '''
    articles = {article: Comment.objects.filter(article=article) for article in Article.objects.all()}
    context = {'articles' : articles}
    
    return render(request, 'article/article.html', context)

def articleCreate(request):
    '''
    Create a new article instance
      1. If method is GET, render an empty form
      2. if method is POST, 
        * validate the form and display error message if the form is invalid
        * else, save it to the model and redirect to the article page
    '''
    template = 'article/articleCreate.html'
    if request.method == 'GET':
        return render(request, template, {'articleForm':ArticleForm()})
    
    #POST
    articleForm = ArticleForm(request.POST)
    if not articleForm.is_valid(): # 驗證輸入的資料格式是否正確
        messages.error(request, '資料格式有誤')
        return render(request, template, {'articleForm':ArticleForm}) # ArticleForm包含使用者輸入的資料及錯誤訊息，如此使用者就不需要重新輸入全部資料，只要修正錯誤訊息即可
    
    articleForm.save()
    messages.success(request, '文章已新增')
    #return article(request) # 跳到article.html頁面重新整理會重複執行上次動作(POST)，會再次送出資料，造成相同資料再次儲存
    # django Post/Redirect/Get設計模式 POST處理結束，呼叫redirect()轉址即可
    return redirect('article:article') #article網頁
    
def articleRead(request, articleId):
    '''
    Read an article
      1. Get the article instance; redirect to the 404 page if not found
      2. Render the articleRead template with the article instance and its
         associated comments
    '''
    article = get_object_or_404(Article, id=articleId)
    context = {
        'article' : article,
        'comments' : Comment.objects.filter(article=article)
    }
    return render(request, 'article/articleRead.html', context)