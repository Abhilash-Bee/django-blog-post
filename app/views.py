from django.shortcuts import render, redirect
from app.forms import CommentForm
from django.urls import reverse

from app.models import Comment, Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'app/index.html', context=context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                parent = request.POST.get('parent')
                parent_obj = Comment.objects.get(id=parent)
                if parent_obj:
                    comment_reply = form.save(commit=False)
                    comment_reply.parent = parent_obj 
                    comment_reply.post = post
                    comment_reply.save()
                    return redirect(reverse('app:post_page', kwargs={'slug':slug}))
            else:
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect(reverse('app:post_page', kwargs={'slug':slug}))

    form = CommentForm()
    comments = post.comments.filter(parent=None)
    post.views += 1
    post.save()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'app/post.html', context=context)