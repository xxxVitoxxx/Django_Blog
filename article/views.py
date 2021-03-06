from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm
from django.contrib import messages
from django.http import Http404
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required

from .serializers import ArticleSerializer
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def article(request):
    '''
    show article page
    '''
    articles = {article: Comment.objects.filter(article=article) for article in Article.objects.all()}
    context = {'articles' : articles}
    
    return render(request, 'article/article.html', context)

@login_required
def articleCreate(request):
    '''
    Create a new article instance
      1. If method is GET, render an empty form
      2. if method is POST, 
        * validate the form and display error message if the form is invalid
        * else, save it to the model and redirect to the article page
    '''
    template = 'article/articleCreateUpdate.html'
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

@login_required
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

@login_required
def articleUpdate(request, articleId):
    '''
    Update the article instance:
      1. Get the article to update; redirect to 404 if not found
      2. If method is GET, render a bound form
      3. If method is POST,
        *  validate the form and render a bound form if the form is invalid
        *  else, save it to the model and redirect to the articleRead page
    '''
    article = get_object_or_404(Article, id=articleId)
    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article)
        return render(request, template, {'articleForm':articleForm})
    
    #POST
    articleForm = ArticleForm(request.POST, instance=article)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})

    articleForm.save()
    messages.success(request, '文章已修改')
    return redirect('article:articleRead', articleId=articleId)

@login_required
def articleDelete(request, articleId):
    '''
    Delete the article instance:
      1. Render the article page if the method is GET
      2. Get the article to delete; redirect to 404 if not found
    '''

    if request.method == 'GET':
        return redirect('article:article')
    
    # POST
    article = get_object_or_404(Article, id=articleId)
    article.delete()
    messages.success(request, '文章已成功刪除')
    return redirect('article:article')

def articleSearch(request):
    '''
    Search for articles:
      1. Get the "searchTerm" from the HTML form
      2. Use "searchTerm" for filtering
    '''
    searchTerm = request.GET.get('searchTerm') # 利用request.GET.get()取的name為searchTerm的輸入欄位值
    # 因request.GET的資料是字典結構，所以用get取出資料，若HTML表單找不到此serchTerm變數則回傳None
    articles = Article.objects.filter(Q(title__icontains=searchTerm) | Q(content__icontains=searchTerm))
    # 查詢標題是否包含serchTerm的輸入值 或 內容是否包含searchTerm的輸入值
    context = {'articles': articles, 'searchTerm': searchTerm} # 'searchTerm': searchTerm 為了讓使用者在查詢關鍵字後關鍵字仍顯示在input上
    return render(request, 'article/articleSearch.html', context)

@login_required
def articleLike(request, articleId):
    '''
    Add the user to the 'likes' field:
      1. Get the article; redirect to 404 if not found
      2. If the user does not exist in the 'likes' field, add him/her
      3. Finally, call articleRead() function to render the article
    '''
    article = get_object_or_404(Article, id=articleId)
    #print(f'username: {request.user.username}') #bird
    #print(f'user: {request.user}') # bird(bird)
    #print(f'article: {article}') # title
    if request.user not in article.likes.all():
        article.likes.add(request.user)
    return articleRead(request, articleId)

@login_required
def commentCreate(request, articleId):
    '''
    Create a comment for an article:
      1. Get the comment from the html form
      2. Store it to database
    '''
    if request.method == 'GET':
        return articleRead(request, articleId)
    
    # POST
    comment = request.POST.get('comment')
    if comment:
        comment.strip()
    if not comment:
        return redirect('article:articleRead', articleId=articleId)
    
    article = get_object_or_404(Article, id=articleId)
    Comment.objects.create(article=article, user=request.user, content=comment)
    return redirect('article:articleRead', articleId=articleId)

@login_required
def commentUpdate(request, commentId):
    '''
    Update a comment:
      1. Get the comment to Update and its article; redirect to 404 if not found
      2. If it is a Get request, return
      3. If the comment/'s author is not the user, return
      4. If comment is empty, delete the comment, else update the comment
    '''
    commentToUpdate = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=commentToUpdate.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)
    
    # POST
    if commentToUpdate.user != request.user:
        messages.error(request, '無權限修改')
        return redirect('article:articleRead', articleId=article.id)

    comment = request.POST.get('comment', '').strip() # 找不到變數return ''在strip()
    if not comment:
        commentToUpdate.delete()
    else:
        commentToUpdate.content = comment
        commentToUpdate.save()
    
    return redirect('article:articleRead', articleId=article.id)

@login_required
def commentDelete(request, commentId):
    '''
    1. Get the comment to update and its article; article to 404 if not found
    2. If it is a 'GET' request, return
    3. if the comment's author is not the user, return
    4. Delete tje comment
    '''
    comment = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=comment.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)
    
    # POST
    if comment.user != request.user:
        messages.error(request, '無刪除權限')
        return redirect('article:articleRead', articleId=article.id)
    
    comment.delete()
    return redirect('article:articleRead', articleId=article.id)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # all methods only superuser can user
    #permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = (IsAuthenticated,)
        return [permission() for permission in self.permission_classes]
        
    def list(self, request, **kwargs):
        users = Article.objects.all()
        serializer = ArticleSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    #[POST]
    #@permission_classes((IsAuthenticated,))
    def create(self, request, **kwargs):
        name = request.data.get('name')
        users = Article.objects.create(name=name)
        serializer = ArticleSerializer(users)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
