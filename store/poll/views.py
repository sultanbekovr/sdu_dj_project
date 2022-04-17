from base64 import urlsafe_b64decode
from functools import cache
from multiprocessing import context
from turtle import title
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import CommentForm, EmailPostForm, SearchForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector


# cache
from django.views.decorators.cache import cache_page


menu = [{'title': "Home", 'url_name': 'home'},
        {'title': "Catalog", 'url_name': 'catalog'},
        {'title': "About us", 'url_name': 'about'},]


def index(request):
    context = {
        'menu': menu, 
        'title': 'Main page'
    }
    return render(request,'poll/index.html', context=context)


def about(request):
    return render(request,'poll/about.html', {'menu': menu,'title': 'About'})

@cache_page(60)
def catalog(request):
    posts = Product.objects.all()
    cats = Category.objects.all()
    
    
    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Catalog',
        'cat_selected': 0,
    }
    
    return render(request,'poll/catalog.html', context=context)


def login(request):
    return HttpResponse("login page")


def show_post(request, post_name):
    product = get_object_or_404(Product, p_title=post_name)
    descr = product.p_description
    photo = product.p_photo
    comments = product.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'product': product,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'poll/detail.html', context=context)


def show_category(request, cat_id):
    posts = Product.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()
    
    if len(posts) == 0:
        raise Http404()
    
    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'By Categories',
        'cat_selected': cat_id,
    }
    
    return render(request, 'poll/catalog.html', context=context)
    
    





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


