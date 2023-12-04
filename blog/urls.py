from django.urls import path
from . import views

urlpatterns = [
  path('', views.postList, name='postList'),
  path('register/', views.register, name='register'),
  path('post/<int:pk>/', views.postDetail, name='postDetail'),
  path('post/new/', views.postNew, name='postNew'),
  path('post/category/<int:id_category>/', views.postFilter, name='postFilter'),
  path('post/<int:pk>/publish/', views.postPublish, name='postPublish'),
  path('post/<pk>/remove/', views.postRemove, name='postRemove'),
  path('post/<pk>/edit/', views.postEdit, name='postEdit'),
  path('post/<pk>/myPosts/', views.myPosts, name='myPosts'),
]