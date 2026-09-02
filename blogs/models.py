from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Category(models.Model):
    Category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.Category_name


STATUS_CHOICES = (
    ("draft", "Draft"),
    ("published", "Published")
)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='uploads/%Y/%m/%d')
    short_description = models.TextField(max_length=500)
    blog_body = models.TextField(max_length=2000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_featured = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_blogs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class About(models.Model):
    about = models.TextField(default="About coming soon")
    about_description = models.TextField(max_length=2555, default="no description allowed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'About'

    def __str__(self):
        return self.about


class SocialLinks(models.Model):
    platform = models.CharField(max_length=25)
    link = models.URLField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Social Links'

    def __str__(self):
        return self.platform

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    facebook_link = models.URLField(max_length=100, blank=True)
    twitter_link = models.URLField(max_length=100, blank=True)
    instagram_link = models.URLField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        
    def __str__(self):
        return f"{self.follower} follows {self.following}"