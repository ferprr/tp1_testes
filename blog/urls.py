from django.urls import path
from . import views

urlpatterns = [
  path('', views.postList, name='postList'),
  path('post/<int:pk>/', views.postDetail, name='postDetail'),
  path('post/new/', views.postNew, name='postNew'),
  path('post/category/<int:id_category>/', views.postFilter, name='postFilter')
]