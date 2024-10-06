from django.db import models
from django.contrib.auth.models import AbstractUser


#Custom user model that extends the default AbstractUser 
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure unique email
    def __str__(self):
        return self.username
    
#Model to represent product categories.    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
# Model to represent products in the e-commerce platform
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
