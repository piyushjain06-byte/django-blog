from django import forms
from django.contrib.auth.models import User
from blogs.models import Category, Blog, UserProfile

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields= '__all__'
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields= ('title','category','featured_image','short_description','blog_body','status','is_featured')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio', 'facebook_link', 'twitter_link', 'instagram_link')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')