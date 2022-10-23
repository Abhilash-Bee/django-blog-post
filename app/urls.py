from django.urls import path

from app.views import post_page, index

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post_page, name='post_page'),
]