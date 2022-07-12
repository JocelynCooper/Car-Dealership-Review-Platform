from django.contrib import admin
from .models import CarModel, CarMake


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('dealer_id', 'name', 'type', 'year')
    search_fields = ['name', 'dealer_id', 'type']


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description', 'establish_date')
    search_fields = ['name', 'description']


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
