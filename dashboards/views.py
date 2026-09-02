from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog, UserProfile
from django.contrib.auth.decorators import login_required
from dashboards.forms import CategoryForm, BlogPostForm, UserProfileForm, EditUserForm
from django.utils.text import slugify


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()

    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def categories(request):
    return render(request, 'dashboard/categories.html')


@login_required(login_url='login')
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():  # fixed: was form.is_valid (missing parentheses)
            form.save()
            return redirect('categories')

    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_category.html', context)


@login_required(login_url='login')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():  # fixed: was form.is_valid (missing parentheses)
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboard/edit_category.html', context)


@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


@login_required(login_url='login')
def posts(request):
    posts = Blog.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, 'dashboard/posts.html', context)


@login_required(login_url='login')
def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
        else:
            print('form is invalid')
            print(form.errors)
    form = BlogPostForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_post.html', context)


@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')

    form = BlogPostForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }
    return render(request, 'dashboard/edit_post.html', context)


@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')

@login_required(login_url='login')
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'dashboard/edit_profile.html', context)

@login_required(login_url='login')
def bookmarked_list(request):
    bookmarked_posts = request.user.bookmarked_blogs.all()
    context = {
        'bookmarked_posts': bookmarked_posts,
    }
    return render(request, 'dashboard/bookmarks.html', context)