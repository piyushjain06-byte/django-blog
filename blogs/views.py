from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Blog, Category, About,Comment
from django.db.models import Q
# Create your views here
def posts_by_category(request, Category_id):
    #fetch the post that belongs to the category with the id category_id
    posts = Blog.objects.filter(category =Category_id )
    # # use try/except block when to do some costum action if the category does not exists
    try:
        category = Category.objects.get(pk = Category_id)
    except:
        #redirect the user to home pag
        return redirect('home')
    
    #use get_object_or_404() when u want to show 404error page if the category does not exist
    # category = get_object_or_404(Category , pk = Category_id)
    context ={
        'posts' : posts,
        'category' : category,
    }
    return render(request, 'posts_by_category.html', context) 

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug = slug, status = 'published')
    if request.method=="POST":
        comment= Comment()
        comment.user=request.user
        comment.blog = single_blog
        comment.comment=request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    
    
    #comments
    comments= Comment.objects.filter(blog=single_blog)
    comment_count=comments.count()
    context ={
        'single_blog' : single_blog,
        'comments': comments,
        'comment_count':comment_count
    }
    return render(request,'blogs.html',context)
    
def about_page(request):
    about= About.objects.all()
    
    context = {
        'about' : about
    }
    return render(request, 'about_page.html', context)

def search(request):
    keyword= request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='published')
    context ={
        'blogs': blogs,
        'keyword': keyword
    }
    return render(request, 'search.html',context)