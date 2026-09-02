from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Blog, Category, About, Comment, UserProfile, Follow
from django.db.models import Q
from django.contrib.auth.models import User
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
    single_blog = get_object_or_404(Blog, slug=slug)
    
    viewed_posts = request.session.get('viewed_posts', [])
    if single_blog.id not in viewed_posts:
        single_blog.views_count += 1
        single_blog.save()
        viewed_posts.append(single_blog.id)
        request.session['viewed_posts'] = list(set(viewed_posts))
        
    is_liked = False
    is_bookmarked = False
    if request.user.is_authenticated:
        if single_blog.likes.filter(id=request.user.id).exists():
            is_liked = True
        if single_blog.bookmarks.filter(id=request.user.id).exists():
            is_bookmarked = True

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
        'comment_count':comment_count,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
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

def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=author)
    
    # get all published blogs by this author
    author_blogs = Blog.objects.filter(author=author, status='published').order_by('-created_at')
    
    followers_count = Follow.objects.filter(following=author).count()
    following_count = Follow.objects.filter(follower=author).count()
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=author).exists()
        
    context = {
        'author': author,
        'user_profile': user_profile,
        'author_blogs': author_blogs,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'author_profile.html', context)

def follow_author(request, username):
    if not request.user.is_authenticated:
        return redirect('login')
        
    author = get_object_or_404(User, username=username)
    
    if request.user != author:
        follow_obj = Follow.objects.filter(follower=request.user, following=author)
        if follow_obj.exists():
            follow_obj.delete()
        else:
            Follow.objects.create(follower=request.user, following=author)
            
    return redirect('author_profile', username=username)

def like_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
        
    blog = get_object_or_404(Blog, pk=pk)
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
        
    next_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(next_url)

def bookmark_post(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
        
    blog = get_object_or_404(Blog, pk=pk)
    if blog.bookmarks.filter(id=request.user.id).exists():
        blog.bookmarks.remove(request.user)
    else:
        blog.bookmarks.add(request.user)
        
    next_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(next_url)