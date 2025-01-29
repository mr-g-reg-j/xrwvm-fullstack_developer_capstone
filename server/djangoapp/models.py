# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Car make name (e.g., Toyota, Ford)
    description = models.TextField(blank=True, null=True)  # Optional description
    country = models.CharField(max_length=50, blank=True, null=True)  # Country of origin
    founded_year = models.IntegerField(blank=True, null=True)  # Year founded

    def __str__(self):
        return f"{self.name} - {self.country if self.country else 'Unknown'}"


# <HINT> Create a Car Make model `class CarMake(models.Model)`:   
class CarModel(models.Model):
    # Car types choices
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TRUCK = 'Truck'
    COUPE = 'Coupe'
    MOPED = 'Moped'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (TRUCK, 'Truck'),
        (COUPE, 'Coupe'),
        (MOPED, 'Moped'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")  # Many-to-One with CarMake
    dealer_id = models.IntegerField()  # Refers to dealer in Cloudant database
    name = models.CharField(max_length=100)  # Car model name
    type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)  # Car type (limited choices)
    year = models.DateField()  # Manufacturing year
    
    # Optional fields
    horsepower = models.IntegerField(blank=True, null=True)  # Engine power
    fuel_type = models.CharField(max_length=50, blank=True, null=True)  # Gasoline, Electric, Hybrid, etc.

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year.year}) - {self.type}"



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
