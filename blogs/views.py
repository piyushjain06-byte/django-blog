from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse 
from .models import Blog, Category

# Create your views here
def posts_by_category(request, Category_id):
    #fetch the post that belongs to the category with the id category_id
    posts = Blog.objects.filter(category =Category_id )
    # use try/except block when to do some costum action if the category does not exists
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