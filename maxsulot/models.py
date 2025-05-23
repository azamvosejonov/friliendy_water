from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Maxsulot(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='maxsulot/image', blank=True, null=True)
    body = models.TextField()
    proce = models.DecimalField(max_digits=10, decimal_places=2)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tags = TaggableManager()
    views_count = models.PositiveIntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Maxsulot, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.title}"



class Contact(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.last_name} - {self.email}"