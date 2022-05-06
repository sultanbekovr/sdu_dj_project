from base64 import urlsafe_b64decode
from dataclasses import field
from itertools import product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from multiprocessing import context
from re import template
from turtle import title
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import CommentForm, EmailPostForm, SearchForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector
from django.db.models import Q




from django.shortcuts import render, redirect
from poll.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


# cache
from django.views.decorators.cache import cache_page


menu = [{'title': "Home", 'url_name': 'home'},
        {'title': "Catalog", 'url_name': 'catalog'},
        {'title': "About us", 'url_name': 'about'},]

 

class HomepageView(ListView):
    model = Product
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'poll/index.html'
    extra_context = {'title': 'Home'}
    
    def get_context_data(self, *, object_liss=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
         
    

class AboutPage(ListView):
    model = Product
    template_name = 'poll/about.html'
    extra_context = {'title': 'About us'}
    
    def get_context_data(self, *, object_liss=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context




# view for show_post  
class ProductDetailView(DetailView):
    model = Product    
   
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    
# create new product 
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product    
    fields = ['p_title','price', 'p_description', 'cat', 'p_photo']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context




# update product
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product    
    fields = ['p_title', 'p_description', 'cat', 'p_photo']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context



class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    form = CommentForm
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False
    
    def product(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            product = self.get_object()
            form.instance.user = request.author
            form.instance.product = product
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context
             









# @cache_page(60)
# def catalog(request):
#     posts = Product.objects.all()
    
    
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Catalog',
#         'cat_selected': 0,
#     }
    
#     return render(request,'poll/catalog.html', context=context)


def login(request):
    return HttpResponse("login page")



def show_post(request, post_slug):
    post = get_object_or_404(Product,slug=post_slug)
    context = {
        'post':post,
        'menu':menu,
        'title':post.p_title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'poll/detail.html', context=context)
# def show_post(request, post_name):
#     product = get_object_or_404(Product, p_title=post_name)
#     descr = product.p_description
#     photo = product.p_photo
#     comments = product.comments.filter(active=True)
#     new_comment = None
#     if request.method == 'POST':
#         # A comment was posted
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.product = product
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#     context = {
#         'product': product,
#         'comments': comments,
#         'new_comment': new_comment,
#         'comment_form': comment_form,
#     }
#     return render(request, 'poll/detail.html', context=context)


class ShowCatsView(ListView):
    model = Product
    template_name = 'poll/catalog.html'
    context_object_name = 'posts'
    
    def get_context_data(self, *, object_liss=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


    # def get_queryset(self):
    #     return Product.objects.filter('cat_id'= kwargs={"cat_id": self.pk} ~Q(status = 'draft'))




# class ProductCategory(ListView):
#     model = Product
#     template_name = 'poll/catalog.html'
#     context_object_name = 'posts'
#     def get_queryset(self):
#         return Product.object.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)
# def show_category(request, cat_id):
#     posts = Product.objects.filter(cat_id=cat_id)
#     if len(posts) == 0:
#         raise Http404()
    
#     context = {
#         'posts': posts,
        
#         'menu': menu,
#         'title': 'By Categories',
#         'cat_selected': cat_id,
#     }
    
#     return render(request, 'poll/catalog.html', context=context)

class TechCategory(ListView):
    model = Product
    template_name = 'poll/catalog.html'
    context_object_name = 'posts'
    paginate_by = 3
    def get_queryset(self):
        return Product.objects.filter(cat_id=self.kwargs['cat_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context
class CatalogView(ListView):

    model = Product
    template_name = 'poll/catalog.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Catalog'
        context['cat_selected'] = 0
      
        return context


    def get_queryset(self):
        return Product.objects.filter(~Q(status = 'draft'))
    
    
    
    





# def categories(request, catid):
#     return HttpResponse(f"Categories<p>{catid}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found :((')


def post_share(request, product_id):
    # Retrieve post by id
    product = get_object_or_404(Product, id=product_id)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                product.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{product.p_title}"
            message = f"Read {product.p_title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'rus.mur2001@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'poll/share.html', {'product': product,
                                                'form': form,
                                                'sent': sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.published.annotate(
                search=SearchVector('p_title', 'p_description'),
            ).filter(search=query)
    return render(request,
                  'poll/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


































@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("catalog")


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("catalog")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("catalog")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("catalog")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("catalog")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'poll/catalog.html')