from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'dealer_id', 'type', 'year')
    list_filter = ('make', 'type', 'year')
    search_fields = ('name', 'make__name', 'dealer_id')
    raw_id_fields = ('make',)
