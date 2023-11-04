from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/') 
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request)
            return redirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def postList(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
  category = Category.objects.all()
  search = request.GET.get('search')
  if search:
    posts = Post.objects.filter(title__icontains = search)
  return render(request, 'blog/postList.html', {'posts': posts, 'category': category})

def postDetail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  search = request.GET.get('search')
  if search:
    posts = Post.objects.filter(title__icontains = search)
  return render(request, 'blog/postDetail.html', {'post': post})

@login_required
def postNew(request):
  if request.method == "POST":
      form = PostForm(request.POST)
      if form.is_valid():
          post = form.save(commit=False)
          post.author = request.user
          #post.published_date = timezone.now()
          post.save()
          form.save_m2m()
          return redirect('postDetail', pk=post.pk)
  else:
      form = PostForm() 
  return render(request, 'blog/postNew.html', {'form': form})

def postFilter(request, id_category):
  posts = Post.objects.filter(category = id_category)
  category = Category.objects.all()
  search = request.GET.get('search')
  if search:
    posts = Post.objects.filter(title__icontains = search)
  return render(request, 'blog/postFilter.html', {'posts': posts, 'category': category}) #retornar só nova lista de postsList filtrado pela categoria

@login_required
def postDraftList(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/postDraftList.html', {'posts': posts})

@login_required
def postPublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('/')

@login_required
def postRemove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')

@login_required
def logout(request):
    logout(request)
    return redirect('/')  # Redirect to your home page or any other page after logout