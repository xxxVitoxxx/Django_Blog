from django.shortcuts import render
#from django.http import HttpResponse
# Create your views here.


def main(request):
    '''
    Show "Hello World"
    return HttpResponse('Hello World')
    '''
    context = {'demo' : 'Django content test'}
    return render(request, 'blog_app/main.html', context)

def about(request):
    return render(request, 'blog_app/about.html')