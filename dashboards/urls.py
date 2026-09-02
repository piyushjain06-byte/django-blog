from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Category CRUD
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),  # removed duplicate
    path('categories/edit/<int:pk>', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>', views.delete_category, name='delete_category'),

    # Blog CRUD
    path('posts/', views.posts, name='posts'),
    path('posts/add', views.add_post, name='add_post'),
    path('posts/edit/<int:pk>', views.edit_post, name='edit_post'),
    path('posts/delete/<int:pk>', views.delete_post, name='delete_post'),

    # Profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Bookmarks
    path('bookmarks/', views.bookmarked_list, name='bookmarked_list'),
]