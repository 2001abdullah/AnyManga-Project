from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Merch(models.Model):
    name=models.CharField(max_length=300)
    price=models.IntegerField(blank=True,null=True)
    category=models.CharField(max_length=200,blank=True,null=True)
    picture=models.ImageField(upload_to='images/',blank=True,null=True,default='images/default.jpg')

    def __str__(self):
        return self.name
class Manga(models.Model):
    name=models.CharField(max_length=300)
    price = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    picture=models.ImageField(upload_to='images/',blank=True,null=True,default='images/default.jpg')

    def __str__(self):
        return self.name


