from django.shortcuts import render, redirect
from app.forms import CommentForm, SubscribeForm
from django.urls import reverse
from app.models import Comment, Post, Tag, Profile, WebsiteMeta
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('app:index'))

    top_posts = Post.objects.all().order_by('-views')[:3]
    recent_posts = Post.objects.all().order_by('-last_updated')[:3]
    form = SubscribeForm()
    featured_post = Post.objects.filter(is_featured=True)
    website_info = None

    if featured_post:
        featured_post = featured_post[0]

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
        'form': form,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'featured_post': featured_post,
        'website_info': website_info,
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

def tag_page(request, slug):
    post_name = Tag.objects.get(slug=slug).name
    top_posts = Tag.objects.get(slug=slug).post.all().order_by('-views')[:2]
    recent_posts = Tag.objects.get(slug=slug).post.all().order_by('-last_updated')[:3]
    other_tags = Tag.objects.exclude(slug=slug)
    context = {
        'post_name': post_name,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'other_tags': other_tags,
    }
    return render(request, 'app/tag.html', context=context)

def author_page(request, slug):
    author = Profile.objects.get(slug=slug)
    top_posts = Post.objects.filter(author=author.user).order_by('-views')[:2]
    recent_posts = Post.objects.filter(author=author.user).order_by('-last_updated')[:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')
    context = {
        'author': author,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'top_authors': top_authors,
    }
    return render(request, 'app/author.html', context=context)

def search_page(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    context = {
        'posts': posts,
        'search_query': search_query,
    }
    return render(request, 'app/search.html', context=context)

def about_page(request):
    website_info = None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {
        "website_info": website_info,
    }
    return render(request, 'app/about.html', context=context)