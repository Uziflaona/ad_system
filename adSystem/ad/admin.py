from django.contrib import admin

from .models import Ad, Region, Street, City, Individual, Type, Offer

admin.site.register(Ad)
admin.site.register(Region)
admin.site.register(Street)
admin.site.register(City)
admin.site.register(Individual)
admin.site.register(Type)
admin.site.register(Offer)

