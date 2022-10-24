from django.urls import path

from app.views import post_page, index, tag_page

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post_page, name='post_page'),
    path('tag/<slug:slug>', tag_page, name='tag_page'),
]