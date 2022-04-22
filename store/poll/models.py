from operator import mod
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    p_title = models.CharField(max_length=250, verbose_name='Product Title')
    p_description = models.TextField(blank=True, verbose_name='Product Description')
    p_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Product photo')
    p_time_create = models.DateTimeField(auto_now_add=True)
    p_time_update = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey('Category', on_delete = models.PROTECT, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post',
                       args=[self.p_title])

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={"post_name": self.p_title})

    class Meta:
        ordering = ('-p_time_create',)

    def __str__(self):
        return self.p_title

    # dgfhsjak
    
class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    ct_category_name = models.CharField(max_length=100, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

        
    def __str__(self):
        return self.ct_category_name
        
    
    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_id": self.pk})


class Comment(models.Model):
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='comments',)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    # def __str__(self):
    #     return f'Comment by {self.name} on {self.post}'
