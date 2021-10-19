from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail

from .forms import UserForm
# Create your views here.

def register(request):
    '''
    Register a new user
    '''
    template = 'acc/register.html'
    if request.method == 'GET':
        return render(request, template, {'userForm':UserForm()})

    # POST
    userForm = UserForm(request.POST)
    print(f'userForm: {userForm}')
    if not userForm.is_valid():
        return render(request, template, {'userForm':userForm})
    
    pwd = request.POST.get('password')
    if len(pwd) < 5:
        messages.error(request, '密碼長度要大於5')
        return render(request, template, {'userForm':userForm})
    userForm.save()
    messages.success(request, '歡迎註冊')

    username = request.POST.get('username')
    password = request.POST.get('password')
    mail = request.POST.get('email')
    send_mail(
        'Django\'s Blog register',
        f'Dear {username}\n感謝你註冊Django\'s Blog,\n現在你可以盡情的撰寫你的文章。\n\nBest wishes\nDjango\'s Blog',
        'chaovitoyu83@gmail.com',
        [mail],
        fail_silently=False,
    )
    print(mail)
    print(username)

    user = authenticate(username=username, password=password)
    auth_login(request, user)
    return redirect('blog_app:about')

def login(request):
    '''
    login as existing user
    '''
    template = 'acc/login.html'
    if request.method == 'GET':
        return render(request, template)

    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password: # server-side validation
        messages.error(request, '請填資料')
        return render(request, template)
    
    user = authenticate(username=username, password=password)
    if not user: # authentication fails
        messages.error(request, '登入失敗')
        return render(request, template)

    # login succcess
    auth_login(request, user)
    messages.success(request, '登入成功')
    return redirect('blog_app:about')

def logout(request):
    '''
    logout the user
    '''
    auth_logout(request)
    messages.success(request, '成功登出')
    return redirect('blog_app:main')