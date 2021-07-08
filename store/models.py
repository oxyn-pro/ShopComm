from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone      # We can use this library as well in order to register the time 

from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200)
    
    def __str__(self):
        if self.name == None:
            return "RandomRegister"
        return self.name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
     
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)  
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    country = models.CharField(max_length=255, null=False)
    region_district = models.CharField(max_length=255, default="", null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True) # or use timezone.now

    def __str__(self):
        return self.address

