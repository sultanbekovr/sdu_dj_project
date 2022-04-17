from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

# app_name = 'poll'
urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('catalog/', cache_page(60)(catalog), name='catalog'),
    
    
    
    path('post/<str:post_name>/', show_post, name='post'),
    path('category/<int:cat_id>/', show_category, name='category'),
    path('share/<int:product_id>', post_share, name='post_share'),

    path('search/', post_search, name='post_search'),

]
