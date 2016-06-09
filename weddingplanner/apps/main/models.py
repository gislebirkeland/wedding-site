from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    spouse_first_name = models.CharField(max_length=255)
    spouse_last_name = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)

class Event(models.Model):
    owner = models.ForeignKey(User)
    date = models.DateField()
    zipcode = models.IntegerField()
    city = models.CharField(max_length=100)
    guests = models.IntegerField()

class Business(models.Model):
    name = models.CharField(max_length=255)
    business_id = models.IntegerField()
    address = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    phone = models.IntegerField()
    cellphone = models.IntegerField()
    email = models.CharField(max_length=100)
    logo = models.ImageField()
    credit = models.IntegerField()

class PriceRequest(models.Model):
    businesses = models.ManyToMany(Business, related_name="price_request")
    event = models.ForeignKey(Event)
    form = models.IntegerField()

class Quote(models.Model):
    price_request = models.ForeignKey(PriceRequest)
    business = models.ForeignKey(business)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    photo1 = models.ImageField()
    photo2 = models.ImageField()
    photo3 = models.ImageField()
    photo4 = models.ImageField()
    photo5 = models.ImageField()

#class BusinessUser(AbstractUser):