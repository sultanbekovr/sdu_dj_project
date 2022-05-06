from django.urls import path, re_path
# from django.views.decorators.cache import cache_page
from django.views.generic import *
from . import views
from .views import *
# app_name = 'poll'


urlpatterns = [
    # path('', index, name='home'),
    path('', HomepageView.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('post/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('catalog/post/new/', ProductCreateView.as_view(), name = 'product-create'),
    path('post/<int:pk>/update/', ProductUpdateView.as_view(), name = 'product-update'),
    path('post/<int:pk>/delete/', ProductDeleteView.as_view(), name = 'product-delete'),
    
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<int:cat_id>/',  TechCategory.as_view(), name='category'),
    
    path('share/<int:product_id>', post_share, name='post_share'),

    path('search/', post_search, name='post_search'),
    
    
    
    
    
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

]
