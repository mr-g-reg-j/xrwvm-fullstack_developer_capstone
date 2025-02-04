from django.contrib import admin
from .models import CarMake, CarModel


# CarModelInline class (allows adding CarModels within 
#CarMake in the admin panel)
class CarModelInline(
    admin.TabularInline
):  # or admin.StackedInline for a different layout
    model = CarModel
    extra = 1  # Number of empty forms shown for adding new models


# CarMakeAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "founded_year")
    search_fields = ("name", "country")
    inlines = [CarModelInline]  # Embeds CarModel inside CarMake in admin panel


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "type", "year", "dealer_id")
    list_filter = ("type", "year", "car_make")
    search_fields = ("name", "car_make__name")


# Register models with Django Admin
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
