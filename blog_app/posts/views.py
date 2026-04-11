from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def create(request):
    if request.method == 'POST':
        Post.objects.create(
            title=request.POST['title'],
            text=request.POST['text']
        )
    return redirect('home')

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'post': post})
