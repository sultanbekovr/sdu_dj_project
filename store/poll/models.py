from operator import mod
from django.db import models
from django.urls import reverse

# Create your models here.


class Product(models.Model):
    p_title = models.CharField(max_length=250, verbose_name='Product Title')
    p_description = models.TextField(blank=True, verbose_name='Product Description')
    p_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Product photo')
    p_time_create = models.DateTimeField(auto_now_add=True)
    p_time_update = models.DateTimeField(auto_now=True)
    p_is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete = models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.p_time_create.year,
                             self.p_time_create.month,
                             self.p_time_create.day,
                             self.cat])

    def __str__(self):
        return self.p_title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={"post_name": self.p_title})
    
    
class Category(models.Model):
    ct_category_name = models.CharField(max_length=100, db_index=True)
        
        
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
