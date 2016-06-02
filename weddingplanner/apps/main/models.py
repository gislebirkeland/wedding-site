from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    spouse_first_name = models.CharField(max_length=255)
    spouse_last_name = models.CharField(max_length=255)
    phone = models.IntegerField()

class Event(models.Model):
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

class Quote(models.Model):
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    photo1 = models.ImageField()
    photo2 = models.ImageField()
    photo3 = models.ImageField()
    photo4 = models.ImageField()
    photo5 = models.ImageField()

class PriceRequest(models.Model):
    form = models.IntegerField()
