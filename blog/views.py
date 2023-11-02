from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm

def postList(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
  return render(request, 'blog/postList.html', {'posts': posts})

def postDetail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/postDetail.html', {'post': post})

def postNew(request):
  form = PostForm()
  return render(request, 'blog/postNew.html', {'form': form})