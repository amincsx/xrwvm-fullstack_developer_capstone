from django.contrib import admin
from .models import CarMake, CarModel

# Register the models to appear in Django admin
admin.site.register(CarMake)
admin.site.register(CarModel)