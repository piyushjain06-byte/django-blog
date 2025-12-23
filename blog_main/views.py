from django.http import HttpResponse 
from django.shortcuts import render
from blogs.models import Category , Blog


def home(request):
    # categories = Category.objects.all()  commented because we use context_processors which is throughout the website
    featured_posts = Blog.objects.filter(is_featured = True).order_by('updated_at')
    posts = Blog.objects.filter(is_featured = False )
    
    context = {
        # 'categories' : categories,  commented because we use context_processors which is throughout the website
        "featured_posts" : featured_posts,
        'posts': posts,
    }
    return render(request , "home.html", context) 