from django.db import models
from django.contrib.auth.models import User


class PenCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.IntegerField(default=0)
    manufacture = models.CharField(max_length=100, default="Gokuldas Gangwani")
    category = models.ForeignKey(PenCategory, on_delete=models.CASCADE, default="1")
    

    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

