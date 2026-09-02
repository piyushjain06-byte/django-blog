from django.urls import path
from . import views

urlpatterns = [
    path('<int:Category_id>/', views.posts_by_category , name ='posts_by_category'),
    path('blog/<int:pk>/like/', views.like_post, name='like_post'),
    path('blog/<int:pk>/bookmark/', views.bookmark_post, name='bookmark_post'),
]
