from django.contrib import admin
from .models import User, Business, Event, Quote, PriceRequest

admin.site.register([
	User, 
	Business, 
	Event, 
	Quote, 
	PriceRequest])