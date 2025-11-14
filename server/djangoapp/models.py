# Uncomment the following imports
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# ===========================
# Car Make Model
# ===========================
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True, null=True)  # Optional extra field
    founded = models.IntegerField(blank=True, null=True)               # Optional extra field

    def __str__(self):
        return self.name  # Return name as string representation

# ===========================
# Car Model Model
# ===========================
class CarModel(models.Model):
    # Many-to-one relationship with CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()  # Refers to dealer created in Cloudant database

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),  # optional extra type
        ('COUPE', 'Coupe')   # optional extra type
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SEDAN')
    
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )
    
    color = models.CharField(max_length=50, blank=True, null=True)  # Optional extra field

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"