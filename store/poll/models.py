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
    p_title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL")
    p_description = models.TextField(blank=True, verbose_name="Текст статьи")
    p_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Product photo')
    p_time_create = models.DateTimeField(auto_now_add=True)
    p_time_update = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey('Category', on_delete = models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
    published = PublishedManager()
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
    




    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug': self.slug})

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={"post_name": self.p_title})

    class Meta:
        ordering = ('-p_time_create',)

    def __str__(self):
        return self.p_title

    
    
class Category(models.Model):
    ct_category_name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL")



        
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    # def __str__(self):
    #     return f'Comment by {self.name} on {self.post}'
