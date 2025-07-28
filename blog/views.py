from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post, Comment
from django.db.models import Q

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def home(request):
    post_list = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
        else:
            form = CommentForm()
        paginator = Paginator(comments, 5)

    return render(request, 'blog/post_detail.html', {'post': post,'comments': comments, 'form': form})

def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    else:
        results = Post.objects.none()

    return render(request, 'blog/search.html', {
        "results": results,
        "query": query
    })
def filter_posts_by_tag(request, tag):
    if tag:
        posts = Post.objects.filter(tags__name__in=[tag])
    else:
        posts = Post.objects.all()

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post-detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=post.pk)
        return render(request, 'blog/post_form.html', {
            'form': form,
            'post': post,
            'editing': True
        })

    form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {
        'form': form,
        'post': post,
        'editing': True
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('post-detail', pk=post.pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog-home')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user and comment.post.author != request.user:
        return redirect('post-detail', pk=comment.post.pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('post-detail', pk=comment.post.pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})