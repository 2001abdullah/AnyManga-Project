from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Merch(models.Model):
    name=models.CharField(max_length=300)
    price=models.IntegerField(blank=True,null=True)
    choices=[
        ('Bags', 'Bags'),
        ('Stationery', 'Stationery'),
        ('Accessories', 'Accessories'),
        ('Clothes', 'Clothes'),
        ('Posters & Wall Art', 'Posters & Wall Art'),
        ('Figures & Statues', 'Figures & Statues'),
    ]
    category=models.CharField(max_length=50, choices=choices,default='Clothes')
    picture=models.ImageField(upload_to='images/',blank=True,null=True,default='images/default.jpg')

    def __str__(self):
        return self.name
class Manga(models.Model):
    name=models.CharField(max_length=300)
    price = models.IntegerField(blank=True, null=True)
    choices=[
        ('Action and Heroism', 'Action and Heroism'),
        ('Shonen (少年) Manga', 'Shonen (少年) Manga'),
        ('Shojo (少女) Manga', 'Shojo (少女) Manga'),
        ('Seinen (青年) Manga', 'Seinen (青年) Manga'),
        ('Josei (女性) Manga', 'Josei (女性) Manga'),
        ('Fantasy and Adventure', 'Fantasy and Adventure'),
        ('Kawaii', 'Kawaii'),
    ]
    category = models.CharField(max_length=50, choices=choices,default='Shonen (少年) Manga')
    description = models.TextField(blank=True, null=True)
    picture=models.ImageField(upload_to='images/',blank=True,null=True,default='images/default.jpg')
    writer=models.CharField(blank=True,null=True)
    volume=models.CharField(blank=True,null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    manga_p=models.ForeignKey(Manga,on_delete=models.CASCADE,blank=True,null=True)
    merch_p = models.ForeignKey(Merch, on_delete=models.CASCADE, blank=True, null=True)
    create_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def save(self, *args, **kwargs):
        # Ensure only one product type is associated
        if self.manga_p and self.merch_p:
            raise ValueError("A cart item cannot have both Manga and Merch.")
        if not self.manga_p and not self.merch_p:
            raise ValueError("A cart item must have either Manga or Merch.")
        super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('bKash', 'bKash'),
        ('Nagad', 'Nagad'),
        ('Rocket', 'Rocket'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ], default='Pending')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)

    def __str__(self):
      return f"Order # {self.user.username} - {self.status}"

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"
