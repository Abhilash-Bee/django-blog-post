from django.urls import path

from app.views import about_page, post_page, index, search_page, tag_page, author_page

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post_page, name='post_page'),
    path('tag/<slug:slug>', tag_page, name='tag_page'),
    path('author/<slug:slug>', author_page, name='author_page'),
    path('search/', search_page, name='search_page'),
    path('about/', about_page, name='about'),
]